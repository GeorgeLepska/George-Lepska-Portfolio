#Final Proj
library(readxl)
Jumpscare <- read_excel("Desktop/Data Analysis/Jumpscare.xlsx")
View(Jumpscare)

library(ggplot2)
library(dplyr)


Jumpscare %>%
  mutate(Underclassmen=ifelse(Underclassmen=="no",0,1))-> Jumpscare

Jumpscare %>%
  mutate(Sex=ifelse(Sex=="F",0,1))-> Jumpscare

Jumpscare <- Jumpscare %>%
  mutate(Assignment_new = as.numeric(factor(Assignment, levels = c("nj", "j", "jna"))))

tapply(Jumpscare$Score, Jumpscare$Assignment, FUN=mean)

mean(Jumpscare$Score)

sd(Jumpscare$Score)

tapply(Jumpscare$Score, Jumpscare$Assignment, FUN=sd)


model=aov(Score~Assignment, data=Jumpscare)
summary(model)

#Since the p value is 0.125 (>0.05), (F(2,27) = 2.246), 
#we fail to reject the null hypothesis.
#there are no significant differences in the mean number of words 
#solved between the different Assignment conditions.

model2=aov(Score~Assignment+Sex+Underclassmen, data=Jumpscare)
summary(model2)

#Since the p value is 0.139 (>0.05), (F(2,25) = 2.138), 
#we fail to reject the null hypothesis.
#there are no significant differences in the mean number of words 
#solved between the different Assignment conditions.

#Since the p value is 0.436 (>0.05), (F(1,25) = 0.626), 
#his suggests that there is no statistically significant difference 
#in the number of words solved based on sex after controlling for 
#the other variables.

#Since the p value is 0.792 (>0.05), (F(1,25) = 0.071), 
#This suggests that there is no statistically significant difference in the number 
#of words solved based on whether participants are underclassmen or not, after
#controlling for the other variables.

pairwise.t.test(Jumpscare$Score, Jumpscare$Assignment, p.adj="none")

#the value 0.664 is greater than 0.05, suggesting that there is not enough evidence 
#to reject the null hypothesis for the comparison between the jump scare group
#and the jumpscare no audio group.

#the value 0.131 is greater than 0.05, suggesting that there is not enough evidence 
#to reject the null hypothesis for the comparison between the No jump scare group
#and the jump scare group.

#the value 0.053 is greater than 0.05, suggesting that there is not enough evidence 
#to reject the null hypothesis for the comparison between the No jump scare group
#and the jump scare no audio group.

ggplot(data=Jumpscare)+
  geom_boxplot(aes(x=Assignment, y=Score))+
  ylab("Words Found")+
  xlab("Group Assignment")+
  ggtitle("# of Words Found Based on Assignment")
  
  
