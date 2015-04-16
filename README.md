# pipe2slack
A simple Python script that allows you to pipe (potentially filtered) input to a Slack channel of your choosing.

It is by no means a comprehensive wrapper to Slack's API; rather, it is most useful for spitting program output into a message as an easy way to notify interested parties on your Slack team.

Setup is easy:

In your ~/.bash_profile, make an alias (and don't forget to source it: `source ~/.bash_profile`)

`alias pipe2slack='python ~/path/to/pipe2slack/slack.py'`

You will also need to customize the `config` file with your emoji and webhook URL; and since the default location is `~/.pipe2slack`, it will save you time typing the command if you copy your config there.

With that out of the way, using pipe2slack is really simple! Some examples:

`echo "something to post" | pipe2slack -c #channel-name`
My personal favorite: `mvn clean install | pipe2slack -c @myuser -r "(FAILURE|BUILD SUCCESS)"`
