#version1; creating scatter plots to show biological replicates correlation on sequenced data. Uses fragcounts 
#Reuben January 2020

#reuben.yaa@kcl.ac.uk ; Wardle lab
#########################################
library(optparse)
library(ggplot2)# for drawing the scatters
library(ggpubr) # for doing the correlations 




option_list <- list(
make_option(c("--fragcounts"),help="data.frame must have 2 and 4 columns representing frag counts for rep1 and 2 respectively", type="character",metavar="fragcounts"),
make_option(c("--outdir"),help="Output file, will be created in the working directory",type="character",metavar="OUTDIR",default= "./scatter_plots"),
make_option(c("--name"),help="name of the condition/test/",type="character",metavar="NAME"))


opt_parser <- OptionParser(option_list = option_list)
opt <- parse_args(opt_parser)

if (is.null(opt$fragcounts))
{
  stop("You haven't specified the data frame")
}

scatter<-function (fragcounts, name, outdir)
{ 
  counts<-read.delim(opt$fragcounts, header=F)
  names(counts)<- c("rep1_start", paste0("rep1_",opt$name), "rep2_start", paste0("rep2_",opt$name))
  d <-counts[!(counts[,2]==0 & counts[,4]==0),]
  png(paste0(opt$name,"_scatter_cor.png"),width=250, height=250)
  s <- ggplot(d, aes(x= d[,2] , y= d[,4])) + geom_point() + scale_y_log10(name=paste0("replicate 1_",opt$name)) +scale_x_log10(name=paste0("replicate 2_",opt$name)) +theme_linedraw()
  s +stat_cor(method = "pearson")
}

scatter()

