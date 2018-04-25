import sys
sys.path.append("E:\code\python\p2018\packages")
import quicky
x=quicky.m_query()
quicky.pql.find("a > 1 and b == @c or not c.d == False")