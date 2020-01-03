from mako.template import Template


class RegMap:
    def __init__(self, name="unnamed_map"):
        self.name = name


if __name__ == "__main__":
    regMap = RegMap()

    # Render template
    t = Template(filename="template.v")
    s = t.render(regMap=regMap)

    # Write to file
    f = open("tmp/output.v", 'w')
    f.write(s)
    f.close()
