dat = read.csv(file="pctgrowth.csv", header=TRUE)
head(dat)

means_anova = tapply(dat$y, INDEX=dat$grp, FUN=mean)
means_anova

library("rjags")

mod_string = " model {
    for (i in 1:length(y)) {
        y[i] ~ dnorm(theta[grp[i]],invsig2)
    }

    for (j in 1:max(grp)) {
        theta[j] ~ dnorm(0.0,invtau2)
    }

    mu ~ dnorm(0,1.0/1.0e6)
    invtau2 ~ dgamma(1.0/2.0, 1.0*3.0/2.0)
    invsig2 ~ dgamma(1.0/2.0, 1.0*3.0/2.0)
    tau2 = 1.0 / invtau2
    tau = sqrt(tau2)
    sig2 = 1.0 / invsig2
    sig = sqrt(sig2)

} "

set.seed(113)

data_jags = as.list(dat)

params = c("theta","mu","tau","sig")

mod = jags.model(textConnection(mod_string), data=data_jags, n.chains=3)
update(mod, 1e3)

mod_sim = coda.samples(model=mod,
                       variable.names=params,
                       n.iter=5e3)
mod_csim = as.mcmc(do.call(rbind, mod_sim))

## convergence diagnostics
plot(mod_sim)

gelman.diag(mod_sim)
autocorr.diag(mod_sim)
autocorr.plot(mod_sim)
effectiveSize(mod_sim)

## compute DIC
dic = dic.samples(mod, n.iter=1e3)

colMeans(mod_csim)
