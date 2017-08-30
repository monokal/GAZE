> _This documentation is currently incomplete, but feel free to contribute!_

## gbuild.sh
At the root of this repository you'll find the [gbuild.sh](https://github.com/monokal/GAZE/blob/master/gbuild.sh) script. This wraps some useful functions for building and testing (currently primitively) GAZE code, Docker Images, documentation, etc.

As always, usage can be seen using the `--help` argument:
```bash
usage: gbuild [-h] {build,test,push,all} ...

GAZE build tool.

positional arguments:
  {build,test,push,all}
    build               build the gazectl Docker Image and documentation
    test                test gazectl functionality
    push                push the gazectl Docker Image, documentation and code
    all                 do all of the above in that order

optional arguments:
  -h, --help            show this help message and exit
```

## Support
If you'd like a hand with anything, there are a couple of support channels available:

* [Gitter Chat](https://gitter.im/gaze-tomc/)
* [GitHub Issues](https://github.com/monokal/GAZE/issues)
