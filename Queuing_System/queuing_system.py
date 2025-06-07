import simpy
import random
from collections import defaultdict
from tabulate import tabulate
import matplotlib.pyplot as plt
import pandas as pd

# -----------------------------
# Theoretical Formulas
# -----------------------------
def theoretical_mm1(lam, mu):
    rho = lam / mu
    Ls = rho / (1 - rho)
    Lq = rho**2 / (1 - rho)
    Ws_hr = 1 / (mu - lam)
    Wq_hr = rho / (mu * (1 - rho))
    Ws_min = Ws_hr * 60
    Wq_min = Wq_hr * 60
    Pn = lambda n: (1 - rho) * rho**n
    return {
        'rho': rho,
        'Ls': Ls,
        'Lq': Lq,
        'Ws_hr': Ws_hr,
        'Ws_min': Ws_min,
        'Wq_hr': Wq_hr,
        'Wq_min': Wq_min,
        'P0': Pn(0),
        'P1': Pn(1),
        'P2': Pn(2),
        'P3': Pn(3)
    }

# -----------------------------
# Simulation Class
# -----------------------------
class MM1Simulator:
    def __init__(self, lam, mu, sim_time=10000):
        self.lam = lam / 60
        self.mu = mu / 60
        self.sim_time = sim_time
        self.env = simpy.Environment()
        self.server = simpy.Resource(self.env, capacity=1)
        self.total_served = 0
        self.total_time_sys = 0.0
        self.total_time_q = 0.0
        self.total_busy = 0.0
        self.state_time = defaultdict(float)
        self.last_time = 0.0
        self.n_in_system = 0
        self.arrival_departure_log = []  # NEW: store (arrival, departure) times

    def run(self):
        self.env.process(self._arrivals())
        self.env.run(until=self.sim_time)
        self.state_time[self.n_in_system] += self.sim_time - self.last_time
        return self._metrics()

    def _arrivals(self):
        while True:
            yield self.env.timeout(random.expovariate(self.lam))
            self.env.process(self._customer())

    def _customer(self):
        arrival = self.env.now
        self._update_state(+1)
        with self.server.request() as req:
            yield req
            wait = self.env.now - arrival
            self.total_time_q += wait
            svc = random.expovariate(self.mu)
            self.total_busy += svc
            yield self.env.timeout(svc)
        self.total_served += 1
        departure = self.env.now
        self.total_time_sys += departure - arrival
        # print(f"Customer arrived at {arrival:.2f}, departed at {departure:.2f}, wait time {wait:.2f} min")
        self.arrival_departure_log.append((arrival, departure))  # NEW: log the times
        self._update_state(-1)

    def _update_state(self, delta):
        now = self.env.now
        self.state_time[self.n_in_system] += now - self.last_time
        self.n_in_system += delta
        self.last_time = now

    def _metrics(self):
        T = self.sim_time
        avg_sys = sum(n * t for n, t in self.state_time.items()) / T
        avg_q = sum(max(0, n-1) * t for n, t in self.state_time.items()) / T
        util = self.total_busy / T
        prop = {n: t / T for n, t in sorted(self.state_time.items())}
        avg_ws_min = self.total_time_sys / self.total_served
        avg_wq_min = self.total_time_q / self.total_served
        return {
            'rho_sim': util,
            'Ls_sim': avg_sys,
            'Lq_sim': avg_q,
            'Ws_sim_hr': avg_ws_min / 60,
            'Ws_sim_min': avg_ws_min,
            'Wq_sim_hr': avg_wq_min / 60,
            'Wq_sim_min': avg_wq_min,
            'Prop': prop,
            'Total_served': self.total_served,
            'Total_busy': self.total_busy,
            'Total_time_sys': self.total_time_sys,
            'Total_time_q': self.total_time_q,
            'ArrivalDepartureLog': self.arrival_departure_log  # NEW: return the log
        }

# -----------------------------
# Main Execution
# -----------------------------
if __name__ == '__main__':
    lam0, mu0 = 4, 12
    th0 = theoretical_mm1(lam0, mu0)
    sim0 = MM1Simulator(lam0, mu0, sim_time=10000).run()

    print("\nTheoretical vs. Simulation (Base Case λ=4, μ=12)")
    tbl1 = [["Metric","Theo","Sim"]]
    tbl1 += [
        ["ρ",f"{th0['rho']:.4f}",f"{sim0['rho_sim']:.4f}"],
        ["Ls",f"{th0['Ls']:.4f}",f"{sim0['Ls_sim']:.4f}"],
        ["Lq",f"{th0['Lq']:.4f}",f"{sim0['Lq_sim']:.4f}"],
        ["Ws_hr",f"{th0['Ws_hr']:.4f}",f"{sim0['Ws_sim_hr']:.4f}"],
        ["Wq_hr",f"{th0['Wq_hr']:.4f}",f"{sim0['Wq_sim_hr']:.4f}"],
        ["Ws_min",f"{th0['Ws_min']:.4f}",f"{sim0['Ws_sim_min']:.4f}"],
        ["Wq_min",f"{th0['Wq_min']:.4f}",f"{sim0['Wq_sim_min']:.4f}"],
        ["P0",f"{th0['P0']:.4f}",f"{sim0['Prop'][0]:.4f}"],
        ["P1",f"{th0['P1']:.4f}",f"{sim0['Prop'][1]:.4f}"],
        ["P2",f"{th0['P2']:.4f}",f"{sim0['Prop'][2]:.4f}"],
        ["P3",f"{th0['P3']:.4f}",f"{sim0['Prop'][3]:.4f}"],
    ]
    print(tabulate(tbl1,headers="firstrow",tablefmt="github"))

    print("\nDetailed Simulation Metrics (Base Case)")
    rows2 = [["Metric","Value"],
             ["Total served",sim0['Total_served']],
             ["Total time in system (min)",f"{sim0['Total_time_sys']:.2f}"],
             ["Total time in queue (min)",f"{sim0['Total_time_q']:.2f}"],
             ["Total busy time (min)",f"{sim0['Total_busy']:.2f}"],
             ["Avg # in system",f"{sim0['Ls_sim']:.4f}"],
             ["Avg # in queue",f"{sim0['Lq_sim']:.4f}"]]
    print(tabulate(rows2,headers="firstrow",tablefmt="github"))
    print("\nTheoretical vs Simulated State Probabilities (Pn):")
    max_n = max(max(th0['P0'], th0['P1'], th0['P2'], th0['P3']), max(sim0['Prop']))  # ensure we cover all n
    n_max_to_display = max(sim0['Prop'].keys())  # adjust based on observed states
    rho = th0['rho']
    Pn_theo = lambda n: (1 - rho) * rho**n

    pn_table = [["n", "Pn (Theo)", "Pn (Sim)"]]
    for n in range(n_max_to_display + 1):
        theo = Pn_theo(n)
        sim = sim0['Prop'].get(n, 0.0)
        pn_table.append([n, f"{theo:.4f}", f"{sim:.4f}"])

    print(tabulate(pn_table, headers="firstrow", tablefmt="github"))


    # print("\nArrival and Departure Times")
    log = sim0['ArrivalDepartureLog']
    # print(tabulate(log, headers=["Arrival", "Departure"], tablefmt="github"))
    df = pd.DataFrame(log, columns=["Arrival", "Departure"])
    df.to_csv("arrival_departure_log.csv", index=False)
    print("\nArrival and departure log written to arrival_departure_log.csv")

    print("\nComparison Across Scenarios")
    scenarios=[("Base",4,12),("Sc1",6,12),("Sc2",10,12)]
    hdr=["Scenario","ρ_th","ρ_sim","Ls_th","Ls_sim","Lq_th","Lq_sim","Ws_th(min)","Ws_sim(min)","Wq_th(min)","Wq_sim(min)"]
    tbl3=[hdr]
    rhos,wq_th,wq_sim=[],[],[]
    for name,lam,mu in scenarios:
        th=theoretical_mm1(lam,mu)
        sm = MM1Simulator(lam, mu, sim_time=10000).run()
        tbl3.append([name,
                     f"{th['rho']:.4f}",f"{sm['rho_sim']:.4f}",
                     f"{th['Ls']:.4f}",f"{sm['Ls_sim']:.4f}",
                     f"{th['Lq']:.4f}",f"{sm['Lq_sim']:.4f}",
                     f"{th['Ws_min']:.4f}",f"{sm['Ws_sim_min']:.4f}",
                     f"{th['Wq_min']:.4f}",f"{sm['Wq_sim_min']:.4f}"])
        rhos.append(th['rho']); wq_th.append(th['Wq_min']); wq_sim.append(sm['Wq_sim_min'])
    print(tabulate(tbl3,headers="firstrow",tablefmt="github"))
    print("\n")

    plt.plot(rhos,wq_th,'o-',label='Theo Wq')
    plt.plot(rhos,wq_sim,'s--',label='Sim Wq')
    plt.xlabel('ρ');plt.ylabel('Wq (min)')
    plt.title('Wq vs ρ');plt.grid(True);plt.legend();plt.show()
