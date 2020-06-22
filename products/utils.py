
def calculate_product_cost(materials, work_tasks, company, product):
    material_total_cost = 0
    for material in list(materials):
        material_total_cost += material.material.base_cost
        if material.material.scalable_cost:
            material_total_cost += material.material.unit_cost * material.units

    work_tasks_hours = 0
    for work_task in list(work_tasks):
        work_tasks_hours += work_task.work_hours

    total_work_cost = work_tasks_hours * company.cost_per_work_hour

    total_product_cost = (total_work_cost + material_total_cost + product.extra_cost)

    return material_total_cost, work_tasks_hours, total_work_cost, total_product_cost
