import numpy as np


class SelectionProcess:
    """ Runs a single candidate selection process using the
    * the Rooney Rule algorithm
    """
    def __init__(self, **kwds):
        """ Takes args in (n_x, n_y, k, l, bias, gen_potentials) """
        # Set attributes
        self.__dict__.update(kwds)

        self.gen_potentials = lambda n: np.random.uniform(0, 1, n)
        self.gen_noise = lambda n: np.random.normal(0, 0.03, n)
        # Generate potentials
        self.xx = self.gen_potentials(self.n_x)
        self.yy = self.gen_potentials(self.n_y)
        self.u_rr = self.u_rr_perceived = self.u_rr_experimental = None
        # Sort the x-candidates by perceived potentials
        self.xx[::-1].sort()
        self.xx_with_noise = (self.xx + self.gen_noise(self.n_x))
        self.xx_perceived = self.bias * self.xx_with_noise
        self.xx_experimental = self.bias * self.xx_with_noise
        # Sort the y-candidates
        self.yy[::-1].sort()
        self.yy_perceived = self.yy + self.gen_noise(self.n_y)
        # Run the selection algorithms
        self.selection_using_rooney()

    def selection_using_rooney(self):
        """ Rooney Rule: At least l X-finalists """
        self.x_count = x_ind = y_ind = self.u_rr = self.u_rr_perceived = self.u_rr_experimental = 0
        for i in range(self.k):
            # If have exhausted list of X-candidates
            if (x_ind >= self.n_x):
                self.u_rr += self.yy[y_ind]
                self.u_rr_perceived += self.yy[y_ind]
                self.u_rr_experimental += self.yy[y_ind]
                y_ind += 1
            # If have exhausted list of Y-candidates
            elif (y_ind >= self.n_y):
                self.u_rr += self.xx[x_ind]
                self.u_rr_perceived += self.xx_perceived[x_ind]
                self.u_rr_experimental += self.xx_experimental[x_ind]
                x_ind += 1
                self.x_count += 1
            ##
            # If the Y-candidate has greater perceived potential and
            #   the number of required X candidates left to be selected
            #   is less than the number of candidates left to be selected,
            #   then choose Y-candidate
            ##
            elif(self.xx_perceived[x_ind] < self.yy[y_ind] and self.l - self.x_count < self.k - i):
                self.u_rr += self.yy[y_ind]
                self.u_rr_perceived += self.yy[y_ind]
                self.u_rr_experimental += self.yy[y_ind]
                y_ind += 1
            # Otherwise, choose X candidate
            else:
                self.u_rr += self.xx[x_ind]
                self.u_rr_perceived += self.xx_perceived[x_ind]
                self.u_rr_experimental += self.xx_experimental[x_ind]
                x_ind += 1
                self.x_count += 1
