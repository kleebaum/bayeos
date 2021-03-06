# plots delay test results as points for PHP implementation
# depends on php-delay-test.r
library('zoo')
library('plotrix')

plot_width = 6.3
plot_height = 8

tmp = ''#-tmp'
eval_max_chunk = F
i_max = 8 # number of writer sleep times (9) / max chunk sizes (8)
ws = c('1.0', '0.5', '0.25', '0.125', '0.1', '0.0625', '0.05', '0.01', '0.0') # writer sleep time
mc = c('20.0', '40.0', '80.0', '160.0', '320.0', '640.0', '1280.0', '2560.0') # max chunk

source('php-delay-test.r')

if (eval_max_chunk) {
    if (tmp == '') title_text = 'PHP - Max Chunk Variation - Raspberry Pi - Home Dir - Writer Only'
    else title_text = 'PHP - Max Chunk Variation - Raspberry Pi - RAM - Writer Only'
} else {
    if (tmp == '') title_text = 'PHP - Writer Sleep Time Variation - Raspberry Pi - Home Dir - Writer Only'
    else title_text = 'PHP - Writer Sleep Time Variation - Raspberry Pi - RAM - Writer Only'
}

if (tmp == '') ylimits = c(0,35) else ylimits = c(0,8)

pdf(paste(device, tmp, '/', plot_name, sep=''), width=plot_width)
op = par(mfrow=c(4,2),mar=c(3.5,3.2,0.3,0.5), oma=c(0,0,3,0))
for (j in c(1:i)) {
    if (eval_max_chunk)
        legend_titel = paste('max chunk:', as.numeric(mc[j]), 'byte', sep=' ')
    else
        legend_titel = paste('WS: ', ws[j], 's', sep='')
    plot(delta[[j]][0:1000]*1000, xlab='', ylab='',
    pch=1, cex=0.5, ylim=ylimits, cex.axis=0.8, col="#555555", xlim=c(1,1000))
    abline (h=mean(delta[[j]])*1000, col='steelblue', lwd=1.5)
    title(ylab=expression(paste(Delta, 't [ms]')),
          xlab='record', mgp=c(2.1,1,0), cex.lab=1)
    legend("topright", horiz=F, x.intersp=0, y.intersp = 1, inset=c(0,0), 
           cex=0.8, bty='o', bg = 'white',
           legend = c(paste("Median =", round(median(delta[[j]])*1000,digits=2), 'ms', sep=' '),
                      paste("Mean =", round(mean(delta[[j]])*1000,digits=2), 'ms', sep=' '),
                      paste("Min =", round(min(delta[[j]])*1000,digits=2), 'ms', sep=' '),
                      paste("Max =", round(max(delta[[j]])*1000,digits=2), 'ms', sep=' '),
                      paste("SD =", round(sd(delta[[j]])*1000,digits=2), 'ms', sep=' ')))
    legend("topleft", legend=legend_titel, bty='o', bg = 'white',
           x.intersp=0, y.intersp = 0.9, inset=c(0,0), cex=0.8)
}
title(title_text, outer=T, cex.main=1.1)
par(op)
dev.off()
