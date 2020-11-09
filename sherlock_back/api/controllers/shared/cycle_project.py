from sherlock_back.api.controllers.cycles import find_project_cycles


def count_cycle_stats(casesCycle):
    current_cycles_stats = dict()
    current_cycles_stats['total_not_executed'] = 0
    current_cycles_stats['total_error'] = 0
    current_cycles_stats['total_blocked'] = 0
    current_cycles_stats['total_passed'] = 0
    current_cycles_stats['total'] = 0

    for item in casesCycle:
        current_cycles_stats['total_{}'.format(item.state_code.value)] += 1
        current_cycles_stats['total'] += 1
    return current_cycles_stats


def count_cycles_for_project(project_id):
    all_project_cycles = find_project_cycles(project_id=project_id, cycle_limit=0)
    return len(all_project_cycles)