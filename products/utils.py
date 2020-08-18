from products.models import MaterialForProduct, WorkTaskForProduct


class ProductSummary:
    def __init__(self, materials, work_tasks, material_cost, work_hours, work_cost):
        self.materials = materials
        self.work_tasks = work_tasks
        self.material_cost = material_cost
        self.work_hours = work_hours
        self.work_cost = work_cost
        self.total_cost = self.material_cost + self.work_cost


def calculate_product_summary(product):
    company = product.company
    material_cost = 0
    materials = list(MaterialForProduct.objects.filter(product=product))
    for material in materials:
        material_cost += calculate_material_for_product(material)
    work_hours = 0
    work_cost = 0

    work_list = list(WorkTaskForProduct.objects.filter(product=product))
    for work_task in work_list:
        c_work_hours, c_work_cost = calculate_work_task_for_product(work_task, company)
        work_hours += c_work_hours
        work_cost += c_work_cost

    return ProductSummary(materials, work_list, material_cost, work_hours, work_cost)


def calculate_material_for_product(material_for_product):
    material = material_for_product.material
    base_cost = material.base_cost
    if material.scalable_cost:
        unit_cost = material.unit_cost
        return base_cost + (unit_cost * material_for_product.units)
    else:
        return base_cost


def calculate_work_task_for_product(work_task_for_product, company):
    work_hours = work_task_for_product.work_hours
    if work_task_for_product.work_type.cost:
        work_cost = (work_task_for_product.work_hours * work_task_for_product.work_type.cost)
    else:
        work_cost = (work_task_for_product.work_hours * company.cost_per_work_hour)
    return work_hours, work_cost
