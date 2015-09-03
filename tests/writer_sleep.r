# compares runtime delays for different writer sleep times
# depends on delay-test.r and php-delay-test.r
library('zoo')
library('plotrix')
library('xtable')

colors = c('#b2182b', '#d73027', '#f46d43', '#fdae61', '#fee090', '#ffffbf',
           '#e0f3f8', '#abd9e9', '#4575b4', '#313695')
plot_width = 6.3
plot_height = 3.4

d = 1 # device [1:Raspberry Pi, 2:btrzx3, 3:btrzx5, 4:Ultrabook]

i_max = 9 # number of writer sleep times on x axes
ws = c('1.0', '0.5', '0.25', '0.125', '0.1', '0.0625', '0.05', '0.01', '0.0') # writer sleep time
mc = c('20.0') # max chunk
#ws = c('0.05', '0.01', '0.0')
#mc = c('2560.0')

eval_max_chunk = F

sm = 1 # sender mode
fm  = 1 # filesytem mode
source('delay-test.r')
delta_wo_ws = delta

fm  = 2 # filesytem mode
source('delay-test.r')
delta_wo_tmp_ws = delta

sm = 2 # sender mode
source('delay-test.r')
delta_process_tmp_ws = delta

fm  = 1 # filesytem mode
source('delay-test.r')
delta_process_ws = delta

sm = 3 # sender mode
source('delay-test.r')
delta_thread_ws = delta

fm  = 2 # filesytem mode
source('delay-test.r')
delta_thread_tmp_ws = delta

tmp = ''
source('php-delay-test.r')
delta_php_ws = delta

tmp = '-tmp'
source('php-delay-test.r')
delta_tmp_php_ws = delta

mean_wo_ws = c()
mean_wo_tmp_ws = c()
mean_process_ws = c()
mean_process_tmp_ws = c()
mean_thread_ws = c()
mean_thread_tmp_ws = c()
mean_php_ws = c()
mean_tmp_php_ws = c()
median_wo_ws = c()
median_wo_tmp_ws = c()
median_process_ws = c()
median_process_tmp_ws = c()
median_thread_ws = c()
median_thread_tmp_ws = c()
median_php_ws = c()
median_tmp_php_ws = c()

for (j in c(1:i)) {
    mean_wo_ws[j] = mean(delta_wo_ws[[j]])
    mean_wo_tmp_ws[j] = mean(delta_wo_tmp_ws[[j]])
    mean_process_ws[j] = mean(delta_process_ws[[j]])
    mean_process_tmp_ws[j] = mean(delta_process_tmp_ws[[j]])
    mean_thread_ws[j] = mean(delta_thread_ws[[j]])
    mean_thread_tmp_ws[j] = mean(delta_thread_tmp_ws[[j]])
    mean_php_ws[j] = mean(delta_php_ws[[j]])
    mean_tmp_php_ws[j] = mean(delta_tmp_php_ws[[j]])
    median_wo_ws[j] = median(delta_wo_ws[[j]])
    median_wo_tmp_ws[j] = median(delta_wo_tmp_ws[[j]])
    median_process_ws[j] = median(delta_process_ws[[j]])
    median_process_tmp_ws[j] = median(delta_process_tmp_ws[[j]])
    median_thread_ws[j] = median(delta_thread_ws[[j]])
    median_thread_tmp_ws[j] = median(delta_thread_tmp_ws[[j]])
    median_php_ws[j] = median(delta_php_ws[[j]])
    median_tmp_php_ws[j] = median(delta_tmp_php_ws[[j]])
}

if (d == 1) {
pdf(paste(devices[d], 'writer_sleep_Python_vs_PHP_mc', as.integer(mc[1]), 'mean_log.pdf', sep='_'), width=plot_width, height=plot_height)
y_min = min(mean_wo_ws, mean_php_ws, mean_wo_tmp_ws, mean_tmp_php_ws)*1000
y_max = max(mean_wo_ws, mean_php_ws, mean_wo_tmp_ws, mean_tmp_php_ws)*1000+0.3 
op = par(mar=c(4.2,4.2,0.3,0.5), oma=c(0,0,0,0))
plot(ws, mean_wo_tmp_ws*1000, type='b', xlab='', ylab='', ylim=c(y_min,y_max), 
     cex=0.7, lwd=2, col=colors[1], pch=16, log='y')
title(ylab=expression(paste('mean ', Delta, 't [ms]')),
      xlab='writer sleep time [s]')
lines(ws, mean_wo_ws*1000, type='b', cex=0.7, lwd=2, col=colors[3], pch=8)
lines(ws, mean_tmp_php_ws*1000, type='b', cex=0.7, lwd=2, col=colors[8], pch=24)
lines(ws, mean_php_ws*1000, type='b', cex=0.7, lwd=2, col=colors[10], pch=22)
legend("topright", horiz=F, x.intersp=0, y.intersp = 1, inset=c(0,0), 
    cex=1,  bty='o', box.lty=1, bg = 'white', lty=47,
    legend = c('Python RAM', 'Python Home Dir', 'PHP RAM', 'PHP Home Dir'), 
    lwd=2, pch = c(16, 8, 24, 22),
    col=c(colors[1], colors[3], colors[8], colors[10]))
par(op)
dev.off()

pdf(paste(devices[d], 'writer_sleep_Python_vs_PHP_mc', as.integer(mc[1]), 'median_log.pdf', sep='_'), width=plot_width, height=plot_height)
y_min = min(median_wo_ws, median_php_ws, median_wo_tmp_ws, median_tmp_php_ws)*1000
y_max = max(median_wo_ws, median_php_ws, median_wo_tmp_ws, median_tmp_php_ws)*1000+0.3 
op = par(mar=c(4.2,4.2,0.3,0.5), oma=c(0,0,0,0))
plot(ws, median_wo_tmp_ws*1000, type='b', xlab='', ylab='', ylim=c(y_min,y_max), 
     cex=0.7, lwd=2, col=colors[1], pch=16, log='y')
title(ylab=expression(paste('median ', Delta, 't [ms]')),
      xlab='writer sleep time [s]')
lines(ws, median_wo_ws*1000, type='b', cex=0.7, lwd=2, col=colors[3], pch=8)
lines(ws, median_tmp_php_ws*1000, type='b', cex=0.7, lwd=2, col=colors[8], pch=24)
lines(ws, median_php_ws*1000, type='b', cex=0.7, lwd=2, col=colors[10], pch=22)
legend("topright", horiz=F, x.intersp=0, y.intersp = 1, inset=c(0,0), 
    cex=1,  bty='o', box.lty=1, bg = 'white', lty=47,
    legend = c('Python RAM', 'Python Home Dir', 'PHP RAM', 'PHP Home Dir'), 
    lwd=2, pch = c(16, 8, 24, 22),
    col=c(colors[1], colors[3], colors[8], colors[10]))
par(op)
dev.off()
}

pdf(paste(devices[d], 'writer_sleep_thread_vs_process_mc', as.integer(mc[1]), 'mean_log.pdf', sep='_'), width=plot_width, height=plot_height)
op = par(mar=c(4.2,4.2,0.3,0.5), oma=c(0,0,0,0))
y_min = min(mean_process_ws, mean_thread_ws, mean_process_tmp_ws, mean_thread_tmp_ws)*1000
y_max = max(mean_process_ws, mean_thread_ws, mean_process_tmp_ws, mean_thread_tmp_ws)*1000 
plot(ws, mean_process_tmp_ws*1000, type='b', xlab='', ylab='', ylim=c(y_min,y_max), 
     cex=0.7, lwd=2, col=colors[1], pch=16, log='y')
title(ylab=expression(paste('mean ', Delta, 't [ms]')),
      xlab='writer sleep time [s]')
lines(ws, mean_process_ws*1000, type='b', cex=0.7, lwd=2, col=colors[3], pch=8)
lines(ws, mean_thread_tmp_ws*1000, type='b', cex=0.7, lwd=2, col=colors[8], pch=24)
lines(ws, mean_thread_ws*1000, type='b', cex=0.7, lwd=2, col=colors[10], pch=22)
legend("topright", horiz=F, x.intersp=0, y.intersp = 1, inset=c(0,0), 
    cex=1,  bty='o', box.lty=1, bg = 'white', lty=47,
    legend = c('Process RAM', 'Process Home Dir', 'Thread RAM', 'Thread Home Dir'), 
    lwd=2, pch = c(16, 8, 24, 22),
    col=c(colors[1], colors[3], colors[8], colors[10]))
par(op)
dev.off()

pdf(paste(devices[d], 'writer_sleep_thread_vs_process_mc', as.integer(mc[1]), 'median_log.pdf', sep='_'), width=plot_width, height=plot_height)
op = par(mar=c(4.2,4.2,0.3,0.5), oma=c(0,0,0,0))
y_min = min(median_process_ws, median_thread_ws, median_process_tmp_ws, median_thread_tmp_ws)*1000
y_max = max(median_process_ws, median_thread_ws, median_process_tmp_ws, median_thread_tmp_ws)*1000 
plot(ws, median_process_tmp_ws*1000, type='b', xlab='', ylab='', ylim=c(y_min,y_max), 
     cex=0.7, lwd=2, col=colors[1], pch=16, log='y')
title(ylab=expression(paste('median ', Delta, 't [ms]')),
      xlab='writer sleep time [s]')
lines(ws, median_process_ws*1000, type='b', cex=0.7, lwd=2, col=colors[3], pch=8)
lines(ws, median_thread_tmp_ws*1000, type='b', cex=0.7, lwd=2, col=colors[8], pch=24)
lines(ws, median_thread_ws*1000, type='b', cex=0.7, lwd=2, col=colors[10], pch=22)
legend("topright", horiz=F, x.intersp=0, y.intersp = 1, inset=c(0,0), 
    cex=1,  bty='o', box.lty=1, bg = 'white', lty=47,
    legend = c('Process RAM', 'Process Home Dir', 'Thread RAM', 'Thread Home Dir'), 
    lwd=2, pch = c(16, 8, 24, 22),
    col=c(colors[1], colors[3], colors[8], colors[10]))
par(op)
dev.off()

pdf(paste(devices[d], 'tmp_writer_sleep_mc', as.integer(mc[1]), 'mean_log.pdf', sep='_'), width=3.85, height=plot_height)
op = par(mar=c(4.2,4.2,0.3,0.5), oma=c(0,0,0,0))#, xpd=TRUE
y_min = min(mean_wo_tmp_ws, mean_process_tmp_ws, mean_thread_tmp_ws)*1000
y_max = max(mean_wo_tmp_ws, mean_process_tmp_ws, mean_thread_tmp_ws)*1000 
plot(ws, mean_process_tmp_ws*1000, type='b', xlab='', ylab='', ylim=c(y_min,y_max), 
     cex=0.7, lwd=2, col=colors[1], pch=16, log='y')
title(ylab=expression(paste('mean ', Delta, 't [ms]')),
      xlab='writer sleep time [s]')#, mgp=c(2.1,1,0), cex.lab=1)
lines(ws, mean_wo_tmp_ws*1000, type='b', cex=0.7, lwd=2, col=colors[10], pch=22)
lines(ws, mean_thread_tmp_ws*1000, type='b', cex=0.7, lwd=2, col=colors[3], pch=8)

legend("topright", horiz=F, x.intersp=0, y.intersp = 1, inset=c(0,0), 
    cex=1,  bty='o', box.lty=1, bg = 'white', lty=47,
    legend = c('Process RAM', 'Thread RAM', 'Writer Only RAM'), 
    lwd=2, pch = c(16, 8, 22),
    col=c(colors[1], colors[3], colors[10]))
par(op)
dev.off()


pdf(paste(devices[d], 'writer_sleep_mc', as.integer(mc[1]), 'mean_log.pdf', sep='_'), width=3.45, height=plot_height)
op = par(mar=c(4.2,2,0.3,0.5), oma=c(0,0,0,0))#, xpd=TRUE)
y_min = min(mean_wo_ws, mean_process_ws, mean_thread_ws)*1000
y_max = max(mean_wo_ws, mean_process_ws, mean_thread_ws)*1000 
plot(ws, mean_process_ws*1000, type='b', xlab='', ylab='', ylim=c(y_min,y_max), 
     cex=0.7, lwd=2, col=colors[1], pch=16, log='y')
title(xlab='writer sleep time [s]')#, mgp=c(2.1,1,0), cex.lab=1)
lines(ws, mean_wo_ws*1000, type='b', cex=0.7, lwd=2, col=colors[10], pch=22)
lines(ws, mean_thread_ws*1000, type='b', cex=0.7, lwd=2, col=colors[3], pch=8)

legend("topright", horiz=F, x.intersp=0, y.intersp = 1, inset=c(0,0), 
    cex=1,  bty='o', box.lty=1, bg = 'white', lty=47,
    legend = c('Process Home Dir', 'Thread Home Dir', 'Writer Only Home Dir'), 
    lwd=2, pch = c(16, 8, 22),
    col=c(colors[1], colors[3], colors[10]))
par(op)
dev.off()

pdf(paste(devices[d], 'tmp_writer_sleep_mc', as.integer(mc[1]), 'median_log.pdf', sep='_'), width=3.85, height=plot_height)
op = par(mar=c(4.2,4.2,0.3,0.5), oma=c(0,0,0,0))#, xpd=TRUE
y_min = min(median_wo_tmp_ws, median_process_tmp_ws, median_thread_tmp_ws)*1000
y_max = max(median_wo_tmp_ws, median_process_tmp_ws, median_thread_tmp_ws)*1000+0.3 
plot(ws, median_process_tmp_ws*1000, type='b', xlab='', ylab='', ylim=c(y_min,y_max), 
     cex=0.7, lwd=2, col=colors[1], pch=16, log='y')
title(ylab=expression(paste('median ', Delta, 't [ms]')),
      xlab='writer sleep time [s]')#, mgp=c(2.1,1,0), cex.lab=1)
lines(ws, median_wo_tmp_ws*1000, type='b', cex=0.7, lwd=2, col=colors[10], pch=22)
lines(ws, median_thread_tmp_ws*1000, type='b', cex=0.7, lwd=2, col=colors[3], pch=8)

legend("topright", horiz=F, x.intersp=0, y.intersp = 1, inset=c(0,0), 
    cex=1,  bty='o', box.lty=1, bg = 'white', lty=47,
    legend = c('Process RAM', 'Thread RAM', 'Writer Only RAM'), 
    lwd=2, pch = c(16, 8, 22),
    col=c(colors[1], colors[3], colors[10]))
par(op)
dev.off()

pdf(paste(devices[d], 'writer_sleep_mc', as.integer(mc[1]), 'median_log.pdf', sep='_'), width=3.45, height=plot_height)
op = par(mar=c(4.2,2,0.3,0.5), oma=c(0,0,0,0))#, xpd=TRUE)
y_min = min(median_wo_ws, median_process_ws, median_thread_ws)*1000
y_max = max(median_wo_ws, median_process_ws, median_thread_ws)*1000 
plot(ws, median_process_ws*1000, type='b', xlab='', ylab='', ylim=c(y_min,y_max), 
     cex=0.7, lwd=2, col=colors[1], pch=16, log='y')
title(xlab='writer sleep time [s]')#, mgp=c(2.1,1,0), cex.lab=1)
lines(ws, median_wo_ws*1000, type='b', cex=0.7, lwd=2, col=colors[10], pch=22)
lines(ws, median_thread_ws*1000, type='b', cex=0.7, lwd=2, col=colors[3], pch=8)

legend("topright", horiz=F, x.intersp=0, y.intersp = 1, inset=c(0,0), 
    cex=1,  bty='o', box.lty=1, bg = 'white', lty=47,
    legend = c('Process Home Dir', 'Thread Home Dir', 'Writer Only Home Dir'), 
    lwd=2, pch = c(16, 8, 22),
    col=c(colors[1], colors[3], colors[10]))
par(op)
dev.off()

####--- calculate differences ---####
median_diff_python = c()
sum_median_diff_python = 0
for (i in c(1:i_max)) {
    median_diff_python[i] = median(delta_wo_ws[[i]]) - median(delta_wo_tmp_ws[[i]])
}
mean(median_diff_python)*1000
sd(median_diff_python)*1000
median(median_diff_python)*1000


median_diff_php = c()
for (i in c(1:i_max)) {
    median_diff_php[i] = median(delta_php_ws[[i]]) - median(delta_tmp_php_ws[[i]])
}
mean(median_diff_php)*1000
median(median_diff_php)*1000


median_diff_php_python_home = c()
for (i in c(1:i_max)) {
    median_diff_php_python_home[i] = median(delta_php_ws[[i]]) - median(delta_wo_ws[[i]])
}
median(median_diff_php_python_home)*1000


median_diff_php_python_ram = c()
for (i in c(1:i_max)) {
    median_diff_php_python_ram[i] = median(delta_tmp_php_ws[[i]]) - median(delta_wo_tmp_ws[[i]])
}
median(median_diff_php_python_ram)*1000

median_diff_python_thread = c()
for (i in c(1:i_max)) {
    median_diff_python_thread[i] = median(delta_thread_tmp_ws[[i]]) - median(delta_thread_ws[[i]])
}
median(median_diff_python_thread)*1000

median_diff_python_process = c()
for (i in c(1:i_max)) {
    median_diff_python_process[i] = median(delta_process_ws[[i]]) - median(delta_process_tmp_ws[[i]])
}
median(median_diff_python_process)*1000

median_diff_python_process_thread_ram = c()
for (i in c(1:i_max)) {
    median_diff_python_process_thread_ram[i] = median(delta_thread_tmp_ws[[i]]) - median(delta_process_tmp_ws[[i]])
}
median(median_diff_python_process_thread_ram)*1000

median_diff_python_process_thread_home = c()
for (i in c(1:i_max)) {
    median_diff_python_process_thread_home[i] = median(delta_thread_ws[[i]]) - median(delta_process_ws[[i]])
}
median(median_diff_python_process_thread_home)*1000

median_diff_python_process_wo_ram = c()
for (i in c(1:i_max)) {
    median_diff_python_process_wo_ram[i] = median(delta_wo_tmp_ws[[i]]) - median(delta_process_tmp_ws[[i]])
}
median(median_diff_python_process_wo_ram)*1000

median_diff_python_process_wo_home = c()
for (i in c(1:i_max)) {
    median_diff_python_process_wo_home[i] = median(delta_wo_ws[[i]]) - median(delta_process_ws[[i]])
}
mean(median_diff_python_process_wo_home)*1000
median(median_diff_python_process_wo_home)*1000

median_diff_python_thread_wo_ram = c()
for (i in c(1:i_max)) {
    median_diff_python_thread_wo_ram[i] = median(delta_wo_tmp_ws[[i]]) - median(delta_thread_tmp_ws[[i]])
}
median(median_diff_python_thread_wo_ram)*1000

median_diff_python_thread_wo_home = c()
for (i in c(1:i_max)) {
    median_diff_python_thread_wo_home[i] = median(delta_wo_ws[[i]]) - median(delta_thread_ws[[i]])
}
mean(median_diff_python_thread_wo_home)*1000
median(median_diff_python_thread_wo_home)*1000

####--- table output --####
table_ws <- data.frame( 'Machine' = character(),
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
    if(d == 1)
    table_ws = rbind(table_ws, cbind(devices[d], sender_modes_long[1], 'PHP', 'RAM', ws[i],
                    round(median(delta_tmp_php_ws[[i]])*1000,2), 
                    round(mean(delta_tmp_php_ws[[i]])*1000,2),
                    round(min(delta_tmp_php_ws[[i]])*1000,2),
                    round(max(delta_tmp_php_ws[[i]])*1000,2),
                    round(sd(delta_tmp_php_ws[[i]])*1000,2)))
    table_ws = rbind(table_ws, cbind(devices[d], sender_modes_long[1], 'Python', 'RAM', ws[i],
                    round(median(delta_wo_tmp_ws[[i]])*1000,2), 
                    round(mean(delta_wo_tmp_ws[[i]])*1000,2),
                    round(min(delta_wo_tmp_ws[[i]])*1000,2),
                    round(max(delta_wo_tmp_ws[[i]])*1000,2),
                    round(sd(delta_wo_tmp_ws[[i]])*1000,2)))
    table_ws = rbind(table_ws, cbind(devices[d], sender_modes_long[2], 'Python', 'RAM', ws[i],
                    round(median(delta_process_tmp_ws[[i]])*1000,2), 
                    round(mean(delta_process_tmp_ws[[i]])*1000,2),
                    round(min(delta_process_tmp_ws[[i]])*1000,2),
                    round(max(delta_process_tmp_ws[[i]])*1000,2),
                    round(sd(delta_process_tmp_ws[[i]])*1000,2)))
    table_ws = rbind(table_ws, cbind(devices[d], sender_modes_long[3], 'Python', 'RAM', ws[i],
                    round(median(delta_thread_tmp_ws[[i]])*1000,2), 
                    round(mean(delta_thread_tmp_ws[[i]])*1000,2),
                    round(min(delta_thread_tmp_ws[[i]])*1000,2),
                    round(max(delta_thread_tmp_ws[[i]])*1000,2),
                    round(sd(delta_thread_tmp_ws[[i]])*1000,2)))
    if (d ==1)
    table_ws = rbind(table_ws, cbind(devices[d], sender_modes_long[1], 'PHP', 'Home Dir', ws[i],
                    round(median(delta_php_ws[[i]])*1000,2), 
                    round(mean(delta_php_ws[[i]])*1000,2),
                    round(min(delta_php_ws[[i]])*1000,2),
                    round(max(delta_php_ws[[i]])*1000,2),
                    round(sd(delta_php_ws[[i]])*1000,2)))
    table_ws = rbind(table_ws, cbind(devices[d], sender_modes_long[1], 'Python', 'Home Dir', ws[i],
                    round(median(delta_wo_ws[[i]])*1000,2), 
                    round(mean(delta_wo_ws[[i]])*1000,2),
                    round(min(delta_wo_ws[[i]])*1000,2),
                    round(max(delta_wo_ws[[i]])*1000,2),
                    round(sd(delta_wo_ws[[i]])*1000,2)))
    table_ws = rbind(table_ws, cbind(devices[d], sender_modes_long[2], 'Python', 'Home Dir', ws[i],
                    round(median(delta_process_ws[[i]])*1000,2), 
                    round(mean(delta_process_ws[[i]])*1000,2),
                    round(min(delta_process_ws[[i]])*1000,2),
                    round(max(delta_process_ws[[i]])*1000,2),
                    round(sd(delta_process_ws[[i]])*1000,2)))
    table_ws = rbind(table_ws, cbind(devices[d], sender_modes_long[3], 'Python', 'Home Dir', ws[i],
                    round(median(delta_thread_ws[[i]])*1000,2), 
                    round(mean(delta_thread_ws[[i]])*1000,2),
                    round(min(delta_thread_ws[[i]])*1000,2),
                    round(max(delta_thread_ws[[i]])*1000,2),
                    round(sd(delta_thread_ws[[i]])*1000,2)))
}

colnames(table_ws) <- c('Machine', 'Sender mode', 'Lang.', 'Path', 'WS [s]', 'Median [ms]', 
                             'Mean [ms]', 'Min [ms]', 'Max [ms]', 'SD [ms]')


print(xtable(table_ws), include.rownames=F)

####--- boxplots ---####
ram = list()
home = list()

for (i in c(1:i_max)) {
ram[[i]] = matrix(c(round(delta_wo_ws[[i]]*1000,2), round(delta_thread_ws[[i]]*1000,2), round(delta_process_ws[[i]]*1000,2)), ncol = 3)
home[[i]] = matrix(c(round(delta_wo_tmp_ws[[i]]*1000,2), round(delta_thread_tmp_ws[[i]]*1000,2), round(delta_process_tmp_ws[[i]]*1000,2)), ncol = 3)
}
pdf(paste(devices[d], '_writer_sleep_boxplots_mc_', mc[1], '.pdf', sep=''), width=plot_width, height=plot_height)    
op = par(mfrow=c(2,i_max),mar=c(2.5,4,1.8,0.5), oma=c(0,0,0,0))

for (i in c(1:i_max)) {
    boxplot(ram[[i]], names = sender_modes_long, outline = F, boxwex = 0.25, cex.axis=1) 
    title_text = paste('WS ', ws[i], 's - RAM', sep='')
    title(title_text, ylab=expression(paste(Delta, 't [ms]')), mgp=c(2.3,1,0), cex.main=1)
}

for (i in c(1:i_max)) {
    boxplot(home[[i]], names = sender_modes_long, outline = F, boxwex = 0.25, cex.axis=1)  
    title_text = paste('WS ', ws[i], 's - Home Dir', sep='')
    title(title_text, ylab=expression(paste(Delta, 't [ms]')), mgp=c(2.3,1,0), cex.main=1)
}

par(op)
dev.off()
