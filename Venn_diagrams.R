#version1; creating Venn diagrams to show interacting fragments(true fragments) shared in 3 conditions, delete one object from the script to get 2 conditions
#overlapp determined using the starting co-ordinates, make sure to direct the script where column with starting cordinates is
#Reuben December 2019

#reuben.yaa@kcl.ac.uk ; Wardle lab
#########################################
library(optparse)
library(Vennerable)



option_list <- list(
make_option(c("--dom_a"),help="data.frame must have 2 columns showing, start and end position of the interactions for 1st condition", type="character",metavar="dom"),
make_option(c("--dom_b"),help="data.frame must have 2 columns showing, start and end position of the interactions for 2nd condition", type="character",metavar="dom"),
make_option(c("--dom_c"),help="data.frame must have 2 columns showing, start and end position of the interactions for 3rd condition", type="character",metavar="dom"),
make_option(c("--outdir"),help="Output file, will be created in the working directory",type="character",metavar="OUTDIR",default= "./venn_diagrams"),
make_option(c("--name_a"),help="name of the 1st condition/test/",type="character",metavar="NAME"),
make_option(c("--name_b"),help="name of the 2nd condition/test/",type="character",metavar="NAME"),
make_option(c("--name_c"),help="name of the 3rd condition/test/",type="character",metavar="NAME")


)

opt_parser <- OptionParser(option_list = option_list)
opt <- parse_args(opt_parser)

if (is.null(opt$dom_a))
{
  stop("You haven't specified the data frame")
}

venn_d <-function (dom_a, dom_b, dom_c, name_a, name_b, name_c, outdir)
{ 
  data_a<-read.delim(opt$dom_a, header=F)
  data_b<-read.delim(opt$dom_b, header=F)
  data_c<-read.delim(opt$dom_c, header=F)
  set_a <-data_a$V2
  set_b <-data_b$V2
  set_c <-data_c$V2
  
  input <- list(set_a, set_b, set_c)
  names(input)<-c(opt$name_a, opt$name_b, opt$name_c)
  Vint <-Venn(input)
 

png(paste0(opt$name_a, "_" , opt$name_b, "_",opt$name_c," venn_diagram.png"),width=2000, height=1000, pointsize=100, res=120)

plot(Vint, doWeights= TRUE)


}

venn_d()

