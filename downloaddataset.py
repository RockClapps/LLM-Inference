from huggingface_hub import snapshot_download

#snapshot_download(repo_id="fddemarco/pushshift-reddit",
#                  local_dir='pushshift',
#                  revision='ce05aed1bdb821a06699f40ad5f91e2a3590b4ee',
#                  repo_type="dataset")

snapshot_download(repo_id="RobinSta/SynthPAI",
                  local_dir='synthpai',
                  revision='b572595f543a51db789caddbb81a9fc4edc6c32f',
                  repo_type="dataset")


