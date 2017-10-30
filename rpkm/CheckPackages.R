# Run this script to check for what packages/libraries are installed on RStudio

ip <- as.data.frame(installed.packages()[,c(1,3:4)])
rownames(ip) <- NULL
ip <- ip[is.na(ip$Priority),1:2,drop=FALSE]
print(ip, row.names=FALSE)

# Uncomment the next line to update all packages
update.packages()

# installing/loading the package:
if(!require(installr)) {
  install.packages("installr"); require(installr)} #load / install+load installr

# using the package:
updateR() # this will start the updating process of your R installation.  It will check for newer versions, and if one is available, will guide you through the decisions you'd need to make.

# If R has been updated, remember to check if there is an update for R studio as well
# Also, reinstall these packages:

# Packages lost during upgrade:

# source("https://bioconductor.org/biocLite.R")
# biocLite()
# biocLite("edgeR")
# install.packages("NBSeq")
# biocLite("qvalue")
# biocLite("systemPipeR")
# install.packages("installr")

# Check version
version