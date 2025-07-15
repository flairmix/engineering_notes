import math

class Pipe_segment:
    pipes = []

    def __init__(self, dn_m, material, length_m=1, isolation_width_m: float = 0.025, isolation_lambda: float = 0.05, tin=65, tout=18):
        self.dn_m = dn_m
        self.material = material
        self.length_m = length_m
        self.isolation_width_m = isolation_width_m
        self.isolation_lambda = isolation_lambda
        self.isolation_d2 = dn_m + (2 * isolation_width_m)
        self.K = 1.2 if self.material == "steel" else 1.7
        self.alpha_is = 10
        self.tin=tin
        self.tout=tout
        self.q_L = round(self.heatloss_pipe_unit())
        self.Qloss_W = round(self.q_L * self.length_m)
        self.pipes.append(self)
    
    def heatloss_pipe_unit(self) -> float:
        
        Ris = ((1/(2*3.1415*self.isolation_lambda)))*(math.log(self.isolation_d2/self.dn_m))
        Ris_L = 1 / (3.1415*self.isolation_d2*self.alpha_is)

        return self.K * (self.tin - self.tout) / (Ris + Ris_L)
    

        
