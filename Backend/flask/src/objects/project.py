class Project():
  def __init__(self, project_id, project_name, recentEvaluation, github_link, project_manager, project_data=None):
    self.project_id = project_id
    self.project_name = project_name
    self.recentEvaluation = recentEvaluation
    self.github_link = github_link
    self.project_manager = project_manager
    self.project_data = project_data