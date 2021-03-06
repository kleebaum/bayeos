# compares runtime delays for different maximum file chunk sizes
# depends on delay-test.r and php-delay-test.r
library('zoo')
library('plotrix')
library('xtable')

colors = c('#b2182b', '#d73027', '#f46d43', '#fdae61', '#fee090', '#ffffbf',
           '#e0f3f8', '#abd9e9', '#4575b4', '#313695')
plot_width = 6.3
plot_height = 3.4

d = 1 # device [1:Raspberry Pi, 2:btrzx3, 3:btrzx5, 4:Ultrabook]

i_max = 8 # number of maximum chunk sizes on x axes
ws = c('1.0') # writer sleep time
mc = c('20.0', '40.0', '80.0', '160.0', '320.0', '640.0', '1280.0', '2560.0') # max chunk

eval_max_chunk = T

sm = 1 # sender mode
fm  = 1 # filesytem mode
source('delay-test.r')
delta_wo_mc = delta

fm  = 2 # filesytem mode
source('delay-test.r')
delta_wo_tmp_mc = delta

sm = 2 # sender mode
source('delay-test.r')
delta_process_tmp_mc = delta

fm  = 1 # filesytem mode
source('delay-test.r')
delta_process_mc = delta

sm = 3 # sender mode
source('delay-test.r')
delta_thread_mc = delta

fm  = 2 # filesytem mode
source('delay-test.r')
delta_thread_tmp_mc = delta

tmp = ''
source('php-delay-test.r')
delta_php_mc = delta

tmp = '-tmp'
source('php-delay-test.r')
delta_tmp_php_mc = delta

mean_wo_mc = c()
mean_wo_tmp_mc = c()
mean_process_mc = c()
mean_process_tmp_mc = c()
mean_thread_mc = c()
mean_thread_tmp_mc = c()
mean_php_mc = c()
mean_tmp_php_mc = c()
median_wo_mc = c()
median_wo_tmp_mc = c()
median_process_mc = c()
median_process_tmp_mc = c()
median_thread_mc = c()
median_thread_tmp_mc = c()
median_php_mc = c()
median_tmp_php_mc = c()

for (j in c(1:i_max)) {
    mean_wo_mc[j] = mean(delta_wo_mc[[j]])
    mean_wo_tmp_mc[j] = mean(delta_wo_tmp_mc[[j]])
    mean_process_mc[j] = mean(delta_process_mc[[j]])
    mean_process_tmp_mc[j] = mean(delta_process_tmp_mc[[j]])
    mean_thread_mc[j] = mean(delta_thread_mc[[j]])
    mean_thread_tmp_mc[j] = mean(delta_thread_tmp_mc[[j]])
    mean_php_mc[j] = mean(delta_php_mc[[j]])
    mean_tmp_php_mc[j] = mean(delta_tmp_php_mc[[j]])
    median_wo_mc[j] = median(delta_wo_mc[[j]])
    median_wo_tmp_mc[j] = median(delta_wo_tmp_mc[[j]])
    median_process_mc[j] = median(delta_process_mc[[j]])
    median_process_tmp_mc[j] = median(delta_process_tmp_mc[[j]])
    median_thread_mc[j] = median(delta_thread_mc[[j]])
    median_thread_tmp_mc[j] = median(delta_thread_tmp_mc[[j]])
    median_php_mc[j] = median(delta_php_mc[[j]])
    median_tmp_php_mc[j] = median(delta_tmp_php_mc[[j]])
}

if (d == 1) {
pdf(paste(devices[d], 'max_chunk_Python_vs_PHP_mean.pdf', sep='_'), width=plot_width, height=plot_height)
op = par(mar=c(4.2,4.2,0.3,0.5), oma=c(0,0,0,0))#, xpd=TRUE)
y_min = min(mean_wo_tmp_mc, mean_tmp_php_mc, mean_wo_mc, mean_php_mc)*1000
y_max = max(mean_wo_tmp_mc, mean_tmp_php_mc, mean_wo_mc, mean_php_mc)*1000 
plot(mc, mean_wo_tmp_mc*1000, type='b', xlab='', ylab='', ylim=c(y_min, y_max), 
     cex=0.7, lwd=2, col=colors[1], pch=16,yaxt="n")
axis(side=2, at=c(seq(from=1,to=9.3,by=1)), labels=c(1,2,3,4,5,6,7,8,9))
title(ylab=expression(paste('mean ', Delta, 't [ms]')),
      xlab='maximum chunk size [bytes]')#, mgp=c(2.1,1,0), cex.lab=1)
lines(mc, mean_wo_mc*1000, type='b', cex=0.7, lwd=2, col=colors[3], pch=8)
lines(mc, mean_tmp_php_mc*1000, type='b', cex=0.7, lwd=2, col=colors[8], pch=24)
lines(mc, mean_php_mc*1000, type='b', cex=0.7, lwd=2, col=colors[10], pch=22)
legend("topright", horiz=F, x.intersp=0, y.intersp = 1, inset=c(0,0), 
    cex=1,  bty='o', box.lty=1, bg = 'white', lty=47,
    legend = c('Python RAM', 'Python Home Dir', 'PHP RAM', 'PHP Home Dir'), 
    lwd=2, pch = c(16, 8, 24, 22),
    col=c(colors[1], colors[3], colors[8], colors[10]))
par(op)
dev.off()

pdf(paste(devices[d], 'max_chunk_Python_vs_PHP_median_log.pdf', sep='_'), width=plot_width, height=plot_height)
op = par(mar=c(4.2,4.2,0.3,0.5), oma=c(0,0,0,0))
y_min = min(median_wo_tmp_mc, median_tmp_php_mc, median_wo_mc, median_php_mc)*1000
y_max = max(median_wo_tmp_mc, median_tmp_php_mc, median_wo_mc, median_php_mc)*1000 
plot(mc, median_wo_tmp_mc*1000, type='b', xlab='', ylab='', ylim=c(y_min, y_max), 
     cex=0.7, lwd=2, col=colors[1], pch=16, log='y')
#axis(side=2, at=c(seq(from=1,to=9.3,by=0.5)), labels=c(1,2,3,4,5,6,7,8,9))
title(ylab=expression(paste('median ', Delta, 't [ms]')),
      xlab='maximum chunk size [bytes]')
lines(mc, median_wo_mc*1000, type='b', cex=0.7, lwd=2, col=colors[3], pch=8)
lines(mc, median_tmp_php_mc*1000, type='b', cex=0.7, lwd=2, col=colors[8], pch=24)
lines(mc, median_php_mc*1000, type='b', cex=0.7, lwd=2, col=colors[10], pch=22)
legend("topright", horiz=F, x.intersp=0, y.intersp = 1, inset=c(0,0), 
    cex=1,  bty='o', box.lty=1, bg = 'white', lty=47,
    legend = c('Python RAM', 'Python Home Dir', 'PHP RAM', 'PHP Home Dir'), 
    lwd=2, pch = c(16, 8, 24, 22),
    col=c(colors[1], colors[3], colors[8], colors[10]))
par(op)
dev.off()
}

pdf(paste(devices[d], 'max_chunk_thread_vs_process_mean_log.pdf', sep='_'), width=plot_width, height=plot_height-0.4)
op = par(mar=c(2.2,4.2,0.3,0.5), oma=c(0,0,0,0))#, xpd=TRUE)
y_min = min(mean_process_tmp_mc, mean_thread_tmp_mc, mean_process_mc, mean_thread_mc)*1000
y_max = max(mean_process_tmp_mc, mean_thread_tmp_mc, mean_process_mc, mean_thread_mc)*1000 
plot(mc, mean_process_tmp_mc*1000, type='b', xlab='', ylab='',
     cex=0.7, lwd=2, col=colors[1], pch=16, log='y', ylim=c(y_min, y_max))
title(ylab=expression(paste('mean ', Delta, 't [ms]')))#,
     # xlab='maximum chunk size [bytes]')#, mgp=c(2.1,1,0), cex.lab=1)
lines(mc, mean_process_mc*1000, type='b', cex=0.7, lwd=2, col=colors[3], pch=8)
lines(mc, mean_thread_tmp_mc*1000, type='b', cex=0.7, lwd=2, col=colors[8], pch=24)
lines(mc, mean_thread_mc*1000, type='b', cex=0.7, lwd=2, col=colors[10], pch=22)

legend("topright", horiz=F, x.intersp=0, y.intersp = 1, inset=c(0,0), 
    cex=1,  bty='o', box.lty=1, bg = 'white', lty=47,
    legend = c('Process RAM', 'Process Home Dir', 'Thread RAM', 'Thread Home Dir'), 
    lwd=2, pch = c(16, 8, 24, 22),
    col=c(colors[1], colors[3], colors[8], colors[10]))
par(op)
dev.off()

pdf(paste(devices[d], 'max_chunk_thread_vs_process_median_log.pdf', sep='_'), width=plot_width, height=plot_height)
op = par(mar=c(4.2,4.2,0.3,0.5), oma=c(0,0,0,0))#, xpd=TRUE)
y_min = min(median_process_tmp_mc, median_thread_tmp_mc, median_process_mc, median_thread_mc)*1000
y_max = max(median_process_tmp_mc, median_thread_tmp_mc, median_process_mc, median_thread_mc)*1000 #+0.5
plot(mc, median_process_tmp_mc*1000, type='b', xlab='', ylab='',
     cex=0.7, lwd=2, col=colors[1], pch=16, log='y', ylim=c(y_min, y_max))
title(ylab=expression(paste('median ', Delta, 't [ms]')),
      xlab='maximum chunk size [bytes]')#, mgp=c(2.1,1,0), cex.lab=1)
lines(mc, median_process_mc*1000, type='b', cex=0.7, lwd=2, col=colors[3], pch=8)
lines(mc, median_thread_tmp_mc*1000, type='b', cex=0.7, lwd=2, col=colors[8], pch=24)
lines(mc, median_thread_mc*1000, type='b', cex=0.7, lwd=2, col=colors[10], pch=22)
legend("topright", horiz=F, x.intersp=0, y.intersp = 1, inset=c(0,0), 
    cex=1,  bty='o', box.lty=1, bg = 'white', lty=47,
    legend = c('Process RAM', 'Process Home Dir', 'Thread RAM', 'Thread Home Dir'), 
    lwd=2, pch = c(16, 8, 24, 22),
    col=c(colors[1], colors[3], colors[8], colors[10]))
par(op)
dev.off()

pdf(paste(devices[d], 'tmp_max_chunk_mean_log.pdf', sep='_'), width=3.85, height=plot_height)
op = par(mar=c(4.2,4.2,0.3,0.5), oma=c(0,0,0,0))#, xpd=TRUE)
y_min = min(mean_wo_tmp_mc, mean_process_tmp_mc, mean_thread_tmp_mc)*1000
y_max = max(mean_wo_tmp_mc, mean_process_tmp_mc, mean_thread_tmp_mc)*1000 
plot(mc, mean_process_tmp_mc*1000, type='b', xlab='', ylab='', ylim=c(y_min,y_max), 
     cex=0.7, lwd=2, col=colors[1], pch=16, log='y')
title(ylab=expression(paste('mean ', Delta, 't [ms]')),
      xlab='maximum chunk size [bytes]')#, mgp=c(2.1,1,0), cex.lab=1)
lines(mc, mean_thread_tmp_mc*1000, type='b', cex=0.7, lwd=2, col=colors[3], pch=8)
lines(mc, mean_wo_tmp_mc*1000, type='b', cex=0.7, lwd=2, col=colors[10], pch=22)
legend("topright", horiz=F, x.intersp=0, y.intersp = 1, inset=c(0,0), 
    cex=1,  bty='o', box.lty=1, bg = 'white', lty=47,
    legend = c('Process RAM', 'Thread RAM', 'Writer Only RAM'), 
    lwd=2, pch = c(16, 8, 22),
    col=c(colors[1], colors[3], colors[10]))
par(op)
dev.off()

pdf(paste(devices[d], 'max_chunk_mean_log.pdf', sep='_'), width=3.45, height=plot_height)
op = par(mar=c(4.2,2,0.3,0.5), oma=c(0,0,0,0))#, xpd=TRUE)
y_min = min(mean_wo_mc, mean_process_mc, mean_thread_mc)*1000
y_max = max(mean_wo_mc, mean_process_mc, mean_thread_mc)*1000 
plot(mc, mean_process_mc*1000, type='b', xlab='', ylab='', ylim=c(y_min, y_max), 
     cex=0.7, lwd=2, col=colors[1], pch=16, log='y')
title(xlab='maximum chunk size [bytes]')#, mgp=c(2.1,1,0), cex.lab=1)
lines(mc, mean_thread_mc*1000, type='b', cex=0.7, lwd=2, col=colors[3], pch=8)
lines(mc, mean_wo_mc*1000, type='b', cex=0.7, lwd=2, col=colors[10], pch=22)
legend("topright", horiz=F, x.intersp=0, y.intersp = 1, inset=c(0,0), 
    cex=1,  bty='o', box.lty=1, bg = 'white', lty=47,
    legend = c('Process Home Dir', 'Thread Home Dir', 'Writer Only Home Dir'), 
    lwd=2, pch = c(16, 8, 22),
    col=c(colors[1], colors[3], colors[10]))
par(op)
dev.off()

pdf(paste(devices[d], 'tmp_max_chunk_median_log.pdf', sep='_'), width=3.85, height=plot_height)
op = par(mar=c(4.2,4.2,0.3,0.5), oma=c(0,0,0,0))#, xpd=TRUE)
y_min = min(median_wo_tmp_mc, median_process_tmp_mc, median_thread_tmp_mc)*1000
y_max = max(median_wo_tmp_mc, median_process_tmp_mc, median_thread_tmp_mc)*1000 #+0.5
plot(mc, median_process_tmp_mc*1000, type='b', xlab='', ylab='', ylim=c(y_min,y_max), 
     cex=0.7, lwd=2, col=colors[1], pch=16, log='y')
title(ylab=expression(paste('median ', Delta, 't [ms]')),
      xlab='maximum chunk size [bytes]')#, mgp=c(2.1,1,0), cex.lab=1)
lines(mc, median_thread_tmp_mc*1000, type='b', cex=0.7, lwd=2, col=colors[3], pch=8)
lines(mc, median_wo_tmp_mc*1000, type='b', cex=0.7, lwd=2, col=colors[10], pch=22)
legend("topright", horiz=F, x.intersp=0, y.intersp = 1, inset=c(0,0), 
    cex=1,  bty='o', box.lty=1, bg = 'white', lty=47,
    legend = c('Process RAM', 'Thread RAM', 'Writer Only RAM'), 
    lwd=2, pch = c(16, 8, 22),
    col=c(colors[1], colors[3], colors[10]))
par(op)
dev.off()

pdf(paste(devices[d], 'max_chunk_median_log.pdf', sep='_'), width=3.45, height=plot_height)
op = par(mar=c(4.2,2,0.3,0.5), oma=c(0,0,0,0))#, xpd=TRUE)
y_min = min(median_wo_mc, median_process_mc, median_thread_mc)*1000
y_max = max(median_wo_mc, median_process_mc, median_thread_mc)*1000+0.1
plot(mc, median_process_mc*1000, type='b', xlab='', ylab='', ylim=c(y_min, y_max), 
     cex=0.7, lwd=2, col=colors[1], pch=16, log='y')
title(xlab='maximum chunk size [bytes]')#, mgp=c(2.1,1,0), cex.lab=1)
lines(mc, median_thread_mc*1000, type='b', cex=0.7, lwd=2, col=colors[3], pch=8)
lines(mc, median_wo_mc*1000, type='b', cex=0.7, lwd=2, col=colors[10], pch=22)
legend("topright", horiz=F, x.intersp=0, y.intersp = 1, inset=c(0,0), 
    cex=1,  bty='o', box.lty=1, bg = 'white', lty=47,
    legend = c('Process Home Dir', 'Thread Home Dir', 'Writer Only Home Dir'), 
    lwd=2, pch = c(16, 8, 22),
    col=c(colors[1], colors[3], colors[10]))
par(op)
dev.off()

####--- calculate median differences ---####
median_diff_python = c()
sum_median_diff_python = 0
for (i in c(1:i_max)) {
    median_diff_python[i] = median(delta_wo_mc[[i]]) - median(delta_wo_tmp_mc[[i]])
}
mean(median_diff_python)*1000
sd(median_diff_python)*1000
median(median_diff_python)*1000


median_diff_php = c()
for (i in c(1:i_max)) {
    median_diff_php[i] = median(delta_php_mc[[i]]) - median(delta_tmp_php_mc[[i]])
}
mean(median_diff_php)*1000
median(median_diff_php)*1000


median_diff_php_python_home = c()
for (i in c(1:i_max)) {
    median_diff_php_python_home[i] = median(delta_php_mc[[i]]) - median(delta_wo_mc[[i]])
}
median(median_diff_php_python_home)*1000


median_diff_php_python_ram = c()
for (i in c(1:i_max)) {
    median_diff_php_python_ram[i] = median(delta_tmp_php_mc[[i]]) - median(delta_wo_tmp_mc[[i]])
}
median(median_diff_php_python_ram)*1000

median_diff_python_thread = c()
for (i in c(1:i_max)) {
    median_diff_python_thread[i] = median(delta_thread_tmp_mc[[i]]) - median(delta_thread_mc[[i]])
}
median(median_diff_python_thread)*1000

median_diff_python_process = c()
for (i in c(1:i_max)) {
    median_diff_python_process[i] = median(delta_process_mc[[i]]) - median(delta_process_tmp_mc[[i]])
}
median(median_diff_python_process)*1000

median_diff_python_process_thread_ram = c()
for (i in c(1:i_max)) {
    median_diff_python_process_thread_ram[i] = median(delta_thread_tmp_mc[[i]]) - median(delta_process_tmp_mc[[i]])
}
median(median_diff_python_process_thread_ram)*1000

median_diff_python_process_thread_home = c()
for (i in c(1:i_max)) {
    median_diff_python_process_thread_home[i] = median(delta_thread_mc[[i]]) - median(delta_process_mc[[i]])
}
median(median_diff_python_process_thread_home)*1000

median_diff_python_process_wo_ram = c()
for (i in c(1:i_max)) {
    median_diff_python_process_wo_ram[i] = median(delta_wo_tmp_mc[[i]]) - median(delta_process_tmp_mc[[i]])
}
median(median_diff_python_process_wo_ram)*1000

median_diff_python_process_wo_home = c()
for (i in c(1:i_max)) {
    median_diff_python_process_wo_home[i] = median(delta_wo_mc[[i]]) - median(delta_process_mc[[i]])
}
median(median_diff_python_process_wo_home)*1000

# ####--- table output ---####
table_mc <- data.frame( 'Machine' = character(),
                        'Sender mode' = character(),
                        'Lang.' = character(),
                        'Path' = character(), 
                        'MC [Byte]' = double(), 
                        'Median [ms]'= double(), 
                        'Mean [ms]'= double(),  
                        'Min [ms]'= double(),  
                        'Max [ms]'= double(),  
                        'SD [ms]' = double())

for (i in c(1:i_max)) {
    if(d==1)
    table_mc = rbind(table_mc, cbind(devices[d], sender_modes_long[1], 'PHP', 'RAM', 20*2^(i-1),
                    round(median(delta_tmp_php_mc[[i]])*1000,2), 
                    round(mean(delta_tmp_php_mc[[i]])*1000,2),
                    round(min(delta_tmp_php_mc[[i]])*1000,2),
                    round(max(delta_tmp_php_mc[[i]])*1000,2),
                    round(sd(delta_tmp_php_mc[[i]])*1000,2)))
    table_mc = rbind(table_mc, cbind(devices[d], sender_modes_long[1], 'Python', 'RAM', 20*2^(i-1),
                    round(median(delta_wo_tmp_mc[[i]])*1000,2), 
                    round(mean(delta_wo_tmp_mc[[i]])*1000,2),
                    round(min(delta_wo_tmp_mc[[i]])*1000,2),
                    round(max(delta_wo_tmp_mc[[i]])*1000,2),
                    round(sd(delta_wo_tmp_mc[[i]])*1000,2)))
    table_mc = rbind(table_mc, cbind(devices[d], sender_modes_long[2], 'Python', 'RAM', 20*2^(i-1),
                    round(median(delta_process_tmp_mc[[i]])*1000,2), 
                    round(mean(delta_process_tmp_mc[[i]])*1000,2),
                    round(min(delta_process_tmp_mc[[i]])*1000,2),
                    round(max(delta_process_tmp_mc[[i]])*1000,2),
                    round(sd(delta_process_tmp_mc[[i]])*1000,2)))
    table_mc = rbind(table_mc, cbind(devices[d], sender_modes_long[3], 'Python', 'RAM', 20*2^(i-1),
                    round(median(delta_thread_tmp_mc[[i]])*1000,2), 
                    round(mean(delta_thread_tmp_mc[[i]])*1000,2),
                    round(min(delta_thread_tmp_mc[[i]])*1000,2),
                    round(max(delta_thread_tmp_mc[[i]])*1000,2),
                    round(sd(delta_thread_tmp_mc[[i]])*1000,2)))
    if(d==1)
    table_mc = rbind(table_mc, cbind(devices[d], sender_modes_long[1], 'PHP', 'Home Dir', 20*2^(i-1),
                    round(median(delta_php_mc[[i]])*1000,2), 
                    round(mean(delta_php_mc[[i]])*1000,2),
                    round(min(delta_php_mc[[i]])*1000,2),
                    round(max(delta_php_mc[[i]])*1000,2),
                    round(sd(delta_php_mc[[i]])*1000,2)))
    table_mc = rbind(table_mc, cbind(devices[d], sender_modes_long[1], 'Python', 'Home Dir', 20*2^(i-1),
                    round(median(delta_wo_mc[[i]])*1000,2), 
                    round(mean(delta_wo_mc[[i]])*1000,2),
                    round(min(delta_wo_mc[[i]])*1000,2),
                    round(max(delta_wo_mc[[i]])*1000,2),
                    round(sd(delta_wo_mc[[i]])*1000,2)))
    table_mc = rbind(table_mc, cbind(devices[d], sender_modes_long[2], 'Python', 'Home Dir', 20*2^(i-1),
                    round(median(delta_process_mc[[i]])*1000,2), 
                    round(mean(delta_process_mc[[i]])*1000,2),
                    round(min(delta_process_mc[[i]])*1000,2),
                    round(max(delta_process_mc[[i]])*1000,2),
                    round(sd(delta_process_mc[[i]])*1000,2)))
    table_mc = rbind(table_mc, cbind(devices[d], sender_modes_long[3], 'Python', 'Home Dir', 20*2^(i-1),
                    round(median(delta_thread_mc[[i]])*1000,2), 
                    round(mean(delta_thread_mc[[i]])*1000,2),
                    round(min(delta_thread_mc[[i]])*1000,2),
                    round(max(delta_thread_mc[[i]])*1000,2),
                    round(sd(delta_thread_mc[[i]])*1000,2)))
}

colnames(table_mc) <- c('Machine', 'Sender mode', 'Lang.', 'Path', 'MC [Byte]', 'Median [ms]', 
                             'Mean [ms]', 'Min [ms]', 'Max [ms]', 'SD [ms]')

print(xtable(table_mc), include.rownames=F)

####--- histogram ---####
pdf(paste(devices[d], 'histograms.pdf', sep='_'), width=plot_width, height=4)
op = par(mfrow=c(2,2),mar=c(3.5,3.2,1.8,0.5), oma=c(0,0,0,0))
hist(delta_wo_tmp_mc[[1]], main='max chunk: 20 byte - RAM', xlab='', ylab='', breaks=20)
title(ylab='Frequency', mgp=c(2.3,1,0))
hist(delta_wo_mc[[1]], main='max chunk: 20 byte - Home Dir', xlab='', ylab='', breaks=20)
hist(delta_wo_tmp_mc[[8]], main='max chunk: 2560 byte - RAM', xlab='', ylab='', breaks=20)
title(ylab='Frequency', xlab=expression(paste(Delta, 't [ms]')), mgp=c(2.3,1,0))
hist(delta_wo_mc[[8]], main='max chunk: 2560 byte - Home Dir', xlab='', ylab='', breaks=20)
title(xlab=expression(paste(Delta, 't [ms]')), mgp=c(2.3,1,0))
par(op)
dev.off()

####--- quantile-quantile plot ---####
pdf(paste(devices[d], 'qqplots.pdf', sep='_'), width=plot_width, height=4)
op = par(mfrow=c(2,2),mar=c(3.5,3.2,1.8,0.5), oma=c(0,0,0,0))
qqnorm(delta_wo_tmp_mc[[1]], main='max chunk: 20 byte - RAM', xlab='', ylab='',
        col="#555555", cex=0.8)
title(ylab='Sample Quantiles', mgp=c(2.3,1,0))
qqline(delta_wo_tmp_mc[[1]])
qqnorm(delta_wo_mc[[1]], main='max chunk: 20 byte - Home Dir', xlab='', ylab='',
        col="#555555", cex=0.8)
qqline(delta_wo_mc[[1]])
qqnorm(delta_wo_tmp_mc[[8]], main='max chunk: 2560 byte - RAM', xlab='', ylab='',
        col="#555555", cex=0.8)
title(ylab='Sample Quantiles', xlab='Theoretical Quantiles', mgp=c(2.3,1,0))
qqline(delta_wo_tmp_mc[[8]])
qqnorm(delta_wo_mc[[8]], main='max chunk: 2560 byte - Home Dir', xlab='', ylab='',
        col="#555555", cex=0.8)
title(xlab='Theoretical Quantiles', mgp=c(2.3,1,0))
qqline(delta_wo_mc[[8]])
par(op)
dev.off()