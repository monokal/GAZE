To make life easy, the `gaze` command-line tool can be used to manage the full stack of media center services. Usage can be seen using the following command:
```sh
gaze --help
```

The `gaze` command-line tool also supports overriding various default runtime arguments using environment variables. Sane defaults have been chosen so you shouldn't need to, but if you do:

*  `GAZECTL_NAMESPACE` - The Docker Namespace of the `gazectl` container (default: `monokal`).
*  `GAZECTL_IMAGE` - The Docker Image of the `gazectl` container (default: `gazectl`).
*  `GAZECTL_VERSION` - The Docker Image Tag of the `gazectl` container (default: `latest`).
*  `GAZECTL_SOCKET` - The Docker socket of the host (default: `/var/run/docker.sock`).
*  `GAZECTL_VOLUMES` - Path to the Docker Volumes mountpoint on the host (default: `/var/lib/docker/volumes`).