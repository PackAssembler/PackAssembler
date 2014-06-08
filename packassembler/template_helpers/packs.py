import packassembler.template_helpers.elements as e


def show_mod_label(context, latest_build, mod_versions):
    outdated_label = e.label('Outdated in Latest Build', 'pull-right label-warning label-mod')
    new_mc_label = e.label('Newer Version Available for Another Minecraft Version', 'pull-right label-default label-mod')
    not_in_build_label = e.label('Not in Latest Build', 'pull-right label-danger label-mod')

    vs = mod_versions[::-1]
    current_version_raw = [i for i in latest_build.mod_versions
                           if i.mod == vs[0].mod]
    if current_version_raw:
        current_version = current_version_raw[0]
        new_vs = vs[0:vs.index(current_version)]

        not_compat = False
        compat = False

        for v in new_vs:
            if latest_build.mc_version == v.mc_version:
                compat = True
            else:
                not_compat = True

        if compat:
            context.write(outdated_label)
        if not_compat:
            context.write(new_mc_label)
    else:
        context.write(not_in_build_label)

    return ''
