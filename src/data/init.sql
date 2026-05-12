CREATE TABLE IF NOT EXISTS clientes_telecom (
    id SERIAL PRIMARY KEY,
    "customerID" VARCHAR(20),
    "gender" VARCHAR(10),
    "SeniorCitizen" INTEGER,
    "Partner" BOOLEAN,
    "Dependents" BOOLEAN,
    "tenure" INTEGER,
    "PhoneService" BOOLEAN,
    "MultipleLines" VARCHAR(30),
    "InternetService" VARCHAR(30),
    "OnlineSecurity" VARCHAR(30),
    "OnlineBackup"  VARCHAR(30),
    "DeviceProtection"  VARCHAR(30),
    "TechSupport"   VARCHAR(30),
    "StreamingTV"   VARCHAR(30),
    "StreamingMovies"   VARCHAR(30),
    "Contract"  VARCHAR(30),
    "PaperlessBilling"  BOOLEAN,
    "PaymentMethod" VARCHAR(30),
    "MonthlyCharges"    INTEGER,
    "TotalCharges"  INTEGER,
    "Churn" BOOLEAN
);


