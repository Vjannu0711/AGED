NSPACE="jbolivar"
APP="energy_data"
VER="0.1.0"
RPORT="6379"
FPORT="5004"
UID="876633"
GID="816966"


list:
	- docker images | grep "jbolivar"
	- docker ps -a | grep ${NAME}

build-api:
	docker build -t jbolivar101/${VER}_api:0.1.0 -f docker/Dockerfile.api .

build-db:
	docker pull redis:6.2.3

build-wrk:	
	docker build -t ${NSPACE}/${APP}-wrk:${VER} \
                     -f docker/Dockerfile.wrk \
                     ./

	

run-api:build-api
	docker run --name ${NSPACE}-api \
                   --network ${NSPACE}-network-test \
                   --env REDIS_IP=${NSPACE}-db \
                   -p ${FPORT}:5000 \
                   -d \
                   ${NSPACE}/${APP}-api:${VER} 
	

run-db: build-db
	docker run --name ${NSPACE}-db \
                   --network ${NSPACE}-network-test \
                   -p ${RPORT}:6379 \
                   -d \
                   -u ${UID}:${GID} \
                   -v ${PWD}/data/:/data \
                   redis:6.2.3

run-wrk: build-wrk
	docker run --name ${NSPACE}-wrk \
                   --network ${NSPACE}-network-test \
                   --env REDIS_IP=${NSPACE}-db \
                   -d \
                   ${NSPACE}/${APP}-wrk:${VER}


rm-api:
	docker stop ${NSPACE}-api && docker rm -f ${NSPACE}-api

rm-db:
	docker stop ${NSPACE}-db && docker rm -f ${NSPACE}-db

rm-wrk:
	docker stop ${NSPACE}-wrk && docker rm -f ${NSPACE}-wrk

cycle-api: rm-api build-api run-api

cycle-db: rm-db build-db run-db

cycle-wrk: rm-wrk build-wrk run-wrk

compose-up:
	VER=${VER} docker-compose -f docker/docker-compose.yml -p ${NSPACE} up -d --build

compose-down:
	VER=${VER} docker-compose -f docker/docker-compose.yml -p ${NSPACE} down
