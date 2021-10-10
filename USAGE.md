# How to use bruv as a docker container

## Preparation

* Choose some directory as the `bruv home` (may be the same as the `bruv
  sources` directory)

* Build the bruv image.
  * In the `bruv sources` directory, run the following command:
    ```bash
    docker build . -t bruv
    ```
  * In case you are using some proxy, add the following arguments to the
    above command:
    ```
    --build-arg http_proxy=http://<proxy host>:<proxy port> \
    --build-arg https_proxy=http://<proxy host>:<proxy port>
    ```

* In the `bruv home` directory, create a file called `bruvrc`. Edit it, and
  set its content to the following:
  ```json
  {
    "username": "<your gerrit username>",
    "host": "<gerrit host ip or name>",
    "port": 29418,
    "private_key": "/opt/private.key",
    "queries": {
      "for-review": "reviewer:self AND is:open",
      "<project name>": "project:<project name> AND is:open"
    },
    "default-queries": ["for-review", "<project name>"],
    "db_file": "/opt/bruv.db",
    "bug_base_urls": {
      "<project name>": "<gerrit UI home>/browse"
    }
  }

* Create a `bruv.db` file (bruv database). In the `bruv home` run the
  following command:
  ```bash
  python3 -c 'import dbm; dbm.open("bruv.db", "c")'
  ```

## Running bruv

* Run the following command:
  ```bash
  docker run --detach --rm -ti --name bruv \
         -v <bruv home>/bruvrc:/root/.bruvrc:Z \
         -v ${HOME}/.ssh/id_rsa:/opt/private.key:Z \
         -v <bruv home>/bruv.db:/opt/bruv.db:Z \
         -p 18081:8080 \
         bruv
  ```
* In case you are using a proxy, add the following arguments before the lines
  starting with `-v`:
  ```
  -e http_proxy="http://<proxy host>:<proxy port>" \
  -e https_proxy="http://<proxy host>:<proxy port>" \
  ```

## Access bruv
* Open a browser at the following address: `http://<you machine ip>:18081`
