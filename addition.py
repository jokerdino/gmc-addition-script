import pandas as pd

# dataframe for reading brokers' data - File name should be "AL_INPUT.xlsx"
df_brokers_data = pd.read_excel("AL_INPUT.xlsx")

# dataframe format for output
df_format = pd.DataFrame(columns=['RiskName','NameoftheInsuredPerson','Relationship','Gender','MaritalStatus','InsuredIdentityNumber','InsuredFamilyMemberIdentityNum','DOB','Age','NomineeName','NomineeRelation','EmploymentStatus','EmploymentCode','DateofJoining','SumInsured','BufferSumInsured','FirstDateofInception','Rate','Premium','DateOfExit','DateofEntry','SerialNumber','CoverTotalSI','CoverTotalPremium','GroupID','GroupSerialNo','LoadingChargeable','CalculatedAmount','BasicPremium','LoadingRateForAvareageAge','TPACode','TPAName','SEQ_NO','RISKSERIAL','FLAGSTATUS'])

# convert Relationship and gender column to category for speed boost
df_brokers_data["Relationship"].astype('category')
df_brokers_data["Gender"].astype('category')

# RiskName, NameoftheInsuredPerson, Relationship, Gender, DOB, Age, EmploymentCode, DateofJoining, SumInsured,
# GroupID, GroupSerialNo, FLAGSTATUS

df_format["NameoftheInsuredPerson"] = (df_brokers_data["NameoftheInsuredPerson"]
                                        .str.rstrip()
                                        .str.replace('.',' ',regex=False)
                                        )
df_format["Relationship"] = df_brokers_data["Relationship"].str.rstrip()

df_format["Gender"] = df_brokers_data["Gender"].str.title()
df_format["DOB"] = df_brokers_data["DOB"].dt.strftime('%d/%m/%Y')
df_format["Age"] = df_brokers_data["Age"]
df_format["EmploymentCode"] = df_brokers_data["EmploymentCode"]
df_format["DateofJoining"] = df_brokers_data["DateofJoining"]
df_format["SumInsured"] = df_brokers_data["SumInsured"]
df_format["GroupID"] = df_format['EmploymentCode']


df_format.loc[df_format["Relationship"].str.contains("Self"),"GroupSerialNo"] = 1
df_format.loc[df_format["Relationship"].str.contains("Spouse"),"GroupSerialNo"] = 2

# group serial number range
# daughter - 10
# son - 15
# sister - 20
# brother - 25

df_format.loc[df_format["Relationship"].str.contains("Daughter"),"GroupSerialNo"] =10
df_format.loc[df_format["Relationship"].str.contains("Son"),"GroupSerialNo"] = 15
df_format.loc[df_format["Relationship"].str.contains("DependentSister"),"GroupSerialNo"] = 20
df_format.loc[df_format["Relationship"].str.contains("DependentBrother"),"GroupSerialNo"] = 25

df_format["GroupSerialNo"] += df_format.groupby(['EmploymentCode',"Relationship"]).cumcount()

df_format["RiskName"] = "Person"
df_format["FLAGSTATUS"] = "A"

df_format.to_excel("addition_upload_format.xlsx",sheet_name="GPA_UPLOAD",index=False)
