FROM mongo:5.0
 # Will be set through Environment Files
 ARG DATABASE_URI
 ARG USERNAME
 ARG PASSWORD


 ENV DATABASE_URI=${DATABASE_URI}
 ENV USERNAME=${USERNAME}
 ENV PASSWORD=${PASSWORD}

 COPY teams.json /teams.json

 COPY players.json /players.json

 COPY disabled_players.json /disabled_players.json

 CMD mongoimport --username ${USERNAME} --password ${PASSWORD} --uri ${DATABASE_URI} --collection teams --drop --jsonArray --file /teams.json && \
     mongoimport --username ${USERNAME} --password ${PASSWORD} --uri ${DATABASE_URI} --collection players --drop --jsonArray --file /players.json && \
     mongoimport --username ${USERNAME} --password ${PASSWORD} --uri ${DATABASE_URI} --collection disabled_players --drop --jsonArray --file /disabled_players.json


 #CMD mongoimport --host mongodb --username --db admin --collection teams --type json --file /teams.json --jsonArray