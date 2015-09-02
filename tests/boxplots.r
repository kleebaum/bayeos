# compares runtime delays for different writer sleep times
library('zoo')
library('plotrix')

colors = c('#b2182b', '#d73027', '#f46d43', '#fdae61', '#fee090', '#ffffbf',
           '#e0f3f8', '#abd9e9', '#4575b4', '#313695')
plot_width = 6.3
plot_height = 4

d = 1 # device

i_max = 3 # number of writer sleep times on x axes
ws = c('0.05', '0.01', '0.0')
mc = c('2560.0')

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

mean_wo_ws = c()
mean_wo_tmp_ws = c()
mean_process_ws = c()
mean_process_tmp_ws = c()
mean_thread_ws = c()
mean_thread_tmp_ws = c()
median_wo_ws = c()
median_wo_tmp_ws = c()
median_process_ws = c()
median_process_tmp_ws = c()
median_thread_tmp_ws = c()
median_thread_ws = c()

for (j in c(1:i)) {
    mean_wo_ws[j] = mean(delta_wo_ws[[j]])
    mean_wo_tmp_ws[j] = mean(delta_wo_tmp_ws[[j]])
    mean_process_ws[j] = mean(delta_process_ws[[j]])
    mean_process_tmp_ws[j] = mean(delta_process_tmp_ws[[j]])
    mean_thread_ws[j] = mean(delta_thread_ws[[j]])
    mean_thread_tmp_ws[j] = mean(delta_thread_tmp_ws[[j]])
    median_wo_ws[j] = median(delta_wo_ws[[j]])
    median_wo_tmp_ws[j] = median(delta_wo_tmp_ws[[j]])
    median_process_ws[j] = median(delta_process_ws[[j]])
    median_process_tmp_ws[j] = median(delta_process_tmp_ws[[j]])
    median_thread_ws[j] = median(delta_thread_ws[[j]])
    median_thread_tmp_ws[j] = median(delta_thread_tmp_ws[[j]])
}

sender_modes_long = c('W. Only', 'Proc.', 'Thread')
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


