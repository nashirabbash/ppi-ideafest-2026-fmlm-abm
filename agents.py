"""
Agent definitions for Mesa Paratransit Simulation.
DriverAgent & PassengerAgent with Stochastic Decision Rules.
"""

import math
import random
import mesa
import config

class DriverAgent(mesa.Agent):
    """
    Paratransit / Angkot Driver Agent.
    Makes operational decisions (speed, dwell time, boycott) based on utility maximization.
    """

    def __init__(self, unique_id, model, arm_config):
        super().__init__(model)
        self.unique_id = unique_id
        self.arm_config = arm_config

        # Spatial & Route State
        self.current_stop_idx = 0
        self.distance_along_stop_km = 0.0
        self.direction = 1  # 1: Outbound to KRL Station, -1: Inbound to Peri-urban neighborhoods
        self.speed_kmh = max(15.0, random.gauss(config.SPEED_KMH_MEAN, config.SPEED_KMH_STD))

        # Vehicle & Operational State
        self.passengers_onboard = []
        self.capacity = config.VEHICLE_CAPACITY
        self.state = "IN_SERVICE"  # "IN_SERVICE", "DWELLING", "BOYCOTTING", "OFFLINE"
        self.dwell_ticks_remaining = 0
        self.current_dwell_duration_min = 0.0
        self.last_served_stop_idx = -1

        # Financial & Performance Log
        self.daily_gross_fare = 0.0
        self.daily_km_traveled = 0.0
        self.daily_bok_cost = 0.0
        self.daily_net_revenue = 0.0
        self.headway_compliance_score = 0.95
        self.safety_score = 0.95
        self.vehicle_condition_score = 0.90
        self.gaming_penalty = 0.0
        self.equity_score = 0.0
        self.net_utility = 0.5
        self.is_boycotting = False

    def step(self):
        """Executed every simulation tick (30 seconds)."""
        if self.is_boycotting:
            self.state = "BOYCOTTING"
            return

        # Update utility & check boycott decision daily or periodically
        if self.model.schedule_tick > 0 and self.model.schedule_tick % (config.TICKS_PER_DAY // 2) == 0:
            self.update_utility_and_decide_boycott()

        if self.is_boycotting:
            self.state = "BOYCOTTING"
            return

        # Manage Dwell State
        if self.state == "DWELLING":
            self.current_dwell_duration_min += (1.0 / config.TICKS_PER_MINUTE)
            self.dwell_ticks_remaining -= 1
            if self.dwell_ticks_remaining <= 0:
                self.state = "IN_SERVICE"
                self.current_dwell_duration_min = 0.0
            return

        # Move vehicle along corridor
        tick_hours = (1.0 / config.TICKS_PER_MINUTE) / 60.0
        distance_step = self.speed_kmh * tick_hours
        self.distance_along_stop_km += distance_step
        self.daily_km_traveled += distance_step
        self.daily_bok_cost += distance_step * config.BOK_PER_KM_IDR

        interval_length_km = config.ROUTE_LENGTH_KM / (config.NUM_STOPS - 1)

        if self.distance_along_stop_km >= interval_length_km:
            self.distance_along_stop_km -= interval_length_km
            self.current_stop_idx += self.direction

            # Turnaround at route endpoints
            if self.current_stop_idx >= config.NUM_STOPS - 1:
                self.current_stop_idx = config.NUM_STOPS - 1
                self.direction = -1
            elif self.current_stop_idx <= 0:
                self.current_stop_idx = 0
                self.direction = 1

            self.service_stop()

    def service_stop(self):
        """Alight and board passengers at current stop, calculate dwell time & anti-gaming penalty."""
        if self.current_stop_idx == self.last_served_stop_idx and self.state == "DWELLING":
            return

        self.last_served_stop_idx = self.current_stop_idx
        stop = self.model.stops[self.current_stop_idx]

        # Alight passengers
        alighting = [p for p in self.passengers_onboard if p.dest_stop_idx == self.current_stop_idx]
        for p in alighting:
            p.state = "ARRIVED"
            p.alight_tick = self.model.schedule_tick
            self.passengers_onboard.remove(p)
            self.model.all_completed_passengers.append(p)

        # Board passengers waiting at stop
        available_seats = self.capacity - len(self.passengers_onboard)
        waiting_pax = stop.get_waiting_passengers()

        boarded_count = 0
        for p in waiting_pax[:available_seats]:
            p.state = "BOARDED"
            p.board_tick = self.model.schedule_tick
            self.passengers_onboard.append(p)
            stop.remove_passenger(p)
            boarded_count += 1
            self.daily_gross_fare += config.FARE_IDR

        # Calculate dwell time (tau)
        base_dwell_mins = 0.4 + (len(alighting) + boarded_count) * 0.05
        queue_len = len(stop.waiting_passengers)
        tau_max = config.TAU_MAX_BASE_MIN + 0.08 * queue_len

        # Dwell decision: Under Arm A & C without anti-gaming, driver dwells excessively ("ngetem")
        if not self.arm_config["anti_gaming"] and queue_len > 2 and not self.arm_config.get("flat_wage", False):
            chosen_dwell_mins = base_dwell_mins + random.uniform(2.5, 6.0)
        else:
            chosen_dwell_mins = base_dwell_mins

        # Telemetry Anti-Gaming Penalty Calculation (Arm D)
        if self.arm_config["anti_gaming"]:
            if chosen_dwell_mins > tau_max:
                excess_dwell = chosen_dwell_mins - tau_max
                self.gaming_penalty = config.ALPHA_GAMING * (excess_dwell ** 2)
            else:
                self.gaming_penalty = 0.0
        else:
            self.gaming_penalty = 0.0

        self.dwell_ticks_remaining = max(1, int(chosen_dwell_mins * config.TICKS_PER_MINUTE))
        if self.dwell_ticks_remaining > 0:
            self.state = "DWELLING"

    def update_utility_and_decide_boycott(self):
        """Calculates Driver Net Utility (U_{i,t}) and boycott decision."""
        if self.arm_config["revenue_floor"]:
            if self.arm_config.get("flat_wage", False):
                # Arm B: Flat Gross Wage
                net_revenue = config.FLAT_BTS_WAGE_IDR - self.daily_bok_cost
                revenue_var = 10000.0 ** 2
            else:
                # Arm D: Net-BOK Revenue Floor Guarantee
                raw_net = self.daily_gross_fare - self.daily_bok_cost
                net_revenue = max(raw_net, config.NET_BOK_REVENUE_FLOOR_IDR)
                revenue_var = 2000.0 ** 2
        else:
            # Arm A & C: Unprotected Raw Fare Revenue
            net_revenue = self.daily_gross_fare - self.daily_bok_cost
            revenue_var = 60000.0 ** 2

        self.daily_net_revenue = net_revenue

        w1, w2, w3 = 0.4, 0.3, 0.3
        raw_s_perf = (w1 * self.headway_compliance_score +
                      w2 * self.safety_score +
                      w3 * self.vehicle_condition_score)

        if self.arm_config["micro_equity"]:
            self.equity_score = max(0.0, raw_s_perf - (self.gaming_penalty * 0.1))
        else:
            self.equity_score = 0.0

        # Utility Function: U_{i,t} = beta_0 + beta_1 * E[R_net] - beta_2 * Var(R) + beta_3 * S_{equity} - gamma * P_{gaming}
        u_net = (config.BETA_0 +
                 config.BETA_1 * net_revenue -
                 config.BETA_2 * revenue_var +
                 config.BETA_3 * self.equity_score -
                 config.GAMMA_GAMING * self.gaming_penalty)

        self.net_utility = u_net

        # Under Arm A (Setoran Tradisi) and Arm C (Unprotected), low revenue and high variance trigger boycott
        if not self.arm_config["revenue_floor"] and u_net < config.BOYCOTT_UTILITY_THRESHOLD:
            if random.random() < 0.12:
                self.is_boycotting = True
                self.state = "BOYCOTTING"


class PassengerAgent:
    """Commuter / Passenger Agent."""

    def __init__(self, unique_id, origin_stop_idx, dest_stop_idx, arrival_tick):
        self.unique_id = unique_id
        self.origin_stop_idx = origin_stop_idx
        self.dest_stop_idx = dest_stop_idx
        self.arrival_tick = arrival_tick
        self.board_tick = None
        self.alight_tick = None
        self.state = "WAITING"

    def get_waiting_time_min(self, current_tick):
        if self.board_tick is not None:
            ticks = self.board_tick - self.arrival_tick
        else:
            ticks = current_tick - self.arrival_tick
        return max(0.1, ticks / config.TICKS_PER_MINUTE)
