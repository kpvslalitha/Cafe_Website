pipeline {
    agent any

    environment {
        EC2_USER = 'ubuntu'                   // or ec2-user for Amazon Linux
        EC2_HOST = '3.82.230.17'
        EC2_KEY  = credentials('my-ec2-key')  // Jenkins SSH credentials
    }

    triggers {
        githubPush()  // 👈 Tells Jenkins to trigger on GitHub push
    }

    stages {
        stage('Clone HTML Site') {
            steps {
                git url: 'https://github.com/kpvslalitha/Cafe_Website.git', branch:'master'
            }
        }

        stage('Deploy Website Files to EC2') {
            steps {
                sh """
                ssh -o StrictHostKeyChecking=no -i ${EC2_KEY} ${EC2_USER}@${EC2_HOST} 'sudo rm -rf /var/www/html/*'
                scp -o StrictHostKeyChecking=no -i ${EC2_KEY} -r * ${EC2_USER}@${EC2_HOST}:/tmp/Cafe_Website/
                ssh -i ${EC2_KEY} ${EC2_USER}@${EC2_HOST} 'sudo cp -r /tmp/Cafe_Website/* /var/www/html/'
                """
            }
        }

        stage('Deploy Flask Service') {
            steps {
                sh """
                # Remove any old temp Flask app directory
                ssh -o StrictHostKeyChecking=no -i ${EC2_KEY} ${EC2_USER}@${EC2_HOST} 'rm -rf /tmp/flask-mail'

                # Copy the Flask app code (from a local directory like ./flask-mail/)
                scp -o StrictHostKeyChecking=no -i ${EC2_KEY} -r flask-mail ${EC2_USER}@${EC2_HOST}:/tmp/

                # Move it to the working directory and start the container
                ssh -i ${EC2_KEY} ${EC2_USER}@${EC2_HOST} '
                sudo rm -rf /var/www/flask-mail &&
                sudo mv /tmp/flask-mail /var/www/ &&
                cd /var/www/flask-mail &&
                sudo docker-compose down || true &&
                sudo docker-compose up -d --build
                '
                """
            }
        }
    }
}
