pipeline {
   agent any
    stages {
        stage('Clone Git') { // clone the repository
            steps {
                git  'https://github.com/inbalLevi/project_covid_19.git' }     
        }
        stage('Run') { // start the script file
            steps {
                sh 'python corona.py' 
            }
        }
        stage ('Test') { // ask for a country input
            script{
                def User_Input = input message: "Enter countries to check COVID-19 data",
                        parameters: [string(defaultValue: '', description: '', name: 'country', trim: false)]

                sh 'curl http://localhost:8080/newCasesPeak?country=${User_Input}'
                sh 'curl http://localhost:8080/recoveredPeak?country=${User_Input}'
                sh 'curl http://localhost:8080/deathsPeak?country=${User_Input}' 
            }   
        }
    }  
}
