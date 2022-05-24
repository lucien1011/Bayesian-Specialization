dat = read.csv(file="callers.csv", header=TRUE)
  ## set R's working directory to the same directory
  ## as this file, or use the full path to the file.

head(dat)
data_jags = as.list(dat)

library("rjags")

mod_string = " model {
	for (i in 1:length(calls)) {
		calls[i] ~ dpois( days_active[i] * lam[i] )
		log(lam[i]) = b0 + b_age*age[i] + b_isgroup2*isgroup2[i]
	}

    b0 ~ dnorm(0.0, 1.0/1e2)
    b_age ~ dnorm(0.0, 1.0/1e2)
    b_isgroup2 ~ dnorm(0.0, 1.0/1e2)
} "

set.seed(102)

params = c('b0','b_age','b_isgroup2')
mod = jags.model(textConnection(mod_string), data=data_jags, n.chains=3)
update(mod, 1e3)

mod_sim = coda.samples(model=mod,
                        variable.names=params,
                        n.iter=5e3)
mod_csim = as.mcmc(do.call(rbind, mod_sim))

head(mod_csim)
mean(mod_csim[,3] > 0)
