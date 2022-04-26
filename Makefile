NAME="jbolivar"
APP="ml_data"
VER="0.1.0"
FPORT="5004"

list:
	- docker images | grep "jbolivar"
	- docker ps -a | grep ${NAME}

build-api:
	docker build -t jbolivar101/${VER}_api:0.1.0 -f docker/Dockerfile.api .

build-db:
	

build-wrk:	


run-api:
	docker run -p ${FPORT}:5000 \
		--name ${NAME}_ml_data_api \
		-d \
		jbolivar101/${APP}_api:${VER} \

run-db:


run-wrk:


rm-api:
	docker rm -f jbolivar_ml_data_api

rm-db:


rm-wrk:


cycle-api: rm-api build-api run-api

cycle-db: rm-db build-db run-db

cycle-wrk: rm-wrk build-wrk run-wrk
