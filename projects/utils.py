from products.utils import calculate_product_summary
from projects.models import ProductForProject


class ProjectSummary:
    def __init__(self, total_hours):
        self.total_hours = total_hours


def calculate_project(project):
    total_hours = 0

    products_for_project_list = list(ProductForProject.objects.filter(project=project))
    for products_for_project in products_for_project_list:
        product_summary = calculate_product_summary(products_for_project.product)
        total_hours += (product_summary.work_hours * products_for_project.quantity)
    return ProjectSummary(total_hours)
