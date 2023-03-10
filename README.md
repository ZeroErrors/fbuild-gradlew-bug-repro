Reproduction case for a bug when using gradle with FASTBuild.

Using FASTBuild v1.09

## Problem:
The FASTBuild `Exec` node makes the child process inherit the current processes stdout, this generally is fine however there are some cases where that process will create a child process of its own which may be long lived and also inherit stdout.
If something using FASTBuild then expects the stdout stream to close it will block and wait for that long lived process that was created.

An example of this is Gradle and the Gradle Daemon. This reproduction case uses `Exec` to call Gradle, Gradle will then spawn the Gradle Daemon process. FASTBuild itself will exit after the `gradlew` process exits so in order to see this problem you need to use the cases listed below.

There are two example cases of this problem. First is a Python script which by itself would be a simple fix to change to first wait for the process to exit and then stop reading stdout however the second case is Visual Studio which also expects stdout to close.

## Reproduction Cases

### Python
Tested with: Python 3.11.2

1. Run the `py fbuild.py -verbose Test`<br/>
You will notice it will execute Gradle and FASTBuild will exit but the Python script is blocked waiting on stdout to close.
2. From a different terminal run `GradleProject/gradlew.bat --stop` to kill the daemon process, and then `fbuild.py` will exit.

### Visual Studio
Tested with: Visual Studio 2022


1. Open the `VSProject/VSProject.sln` solution.
2. Press F5 to build the solution.<br/>
FASTBuild will run and then exit but Visual Studio will still wait.
3. Run `GradleProject/gradlew.bat --stop` to kill the daemon process, the build will then complete in Visual Studio.
