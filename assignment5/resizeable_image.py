'''
Naive_seam and r_seam created by Professor Noah Daniels.
'''



import imagematrix
import timeit

    



class ResizeableImage(imagematrix.ImageMatrix):


    def naive_seam(self, energies):
        seams = []
        for c in range(self.width):
            seams.extend(self.r_seam(c, 0, energies))
        return min(seams)[1]

    def r_seam(self, c, r, energies):
        if r == self.height-1: # base case
            return [(energies[c,r], [(c,r)])]
        children = ([] if c == 0 else self.r_seam(c-1, r+1, energies)) + \
                   (self.r_seam(c, r+1, energies)) + \
                    ([] if c == self.width-1 else self.r_seam(c+1, r+1, energies))
        return [(energies[c,r] + e, l + [(c,r)]) for (e,l) in children]



    def best_seam(self, dp=False):
        energies = {}
        return self.naive_seam(energies)
        raise NotImplementedError

        
    
    def best_seam(self, dp=True):
        dp=dict()
        for j in range(self.height):
            for i in range(self.width):
                if j==0: dp[i,j]=self.energy(i,j),None
                elif self.width==1:
                    dp[i,j]=dp[i,j-1][0]+self.energy(i,j),(i,j-1)
                elif i==0:
                    x=min([(dp[i,j-1][0],(i,j-1)),(dp[i+1,j-1][0],(i+1,j-1))])
                    dp[i,j]=x[0]+self.energy(i,j),x[1]
                elif i==self.width-1:
                    x=min([(dp[i,j-1][0],(i,j-1)),(dp[i-1,j-1][0],(i-1,j-1))])
                    dp[i,j]=x[0]+self.energy(i,j),x[1]
                else:
                    x=min([(dp[i,j-1][0],(i,j-1)),(dp[i+1,j-1][0],(i+1,j-1)),(dp[i-1,j-1][0],(i-1,j-1))])
                    dp[i,j]=x[0]+self.energy(i,j),x[1]
        path=[]
        lil=min([(dp[i,self.height-1][0],i) for i in range(self.width)])
        x=lil[1],self.height-1
        while x is not None:
            path.append(x)
            x=dp[x][1]
        path.reverse()
        return path
        raise NotImplemented
    
    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
