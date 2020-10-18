from django.db import models
import json

class SelectionProcess(models.Model):
    n_x = models.IntegerField(default=20)
    n_y = models.IntegerField(default=20)
    k = models.IntegerField(default=5)
    l = models.IntegerField(default=2)
    bias = models.FloatField(default=0.75)
    is_x = models.TextField(default="")
    true_utils = models.TextField(default="")
    perc_utils = models.TextField(default="")

    def get_is_x(self):
        return json.loads(self.is_x)

    def get_true_utils(self):
        return json.loads(self.true_utils)

    def get_perc_utils(self):
        return json.loads(self.perc_utils)


class ResultHIT(models.Model):
    true_utility = models.TextField(default="")
    perc_utility = models.TextField(default="")
    num_selected_x_cands = models.TextField(default="")
    sp_entry_id = models.TextField(default="")

    def get_true_utility(self):
        return json.loads(self.true_utility)

    def get_perc_utility(self):
        return json.loads(self.perc_utility)

    def get_num_selected_x_cands(self):
        return json.loads(self.num_selected_x_cands)

    def get_sp_entry_id(self):
        return json.loads(self.sp_entry_id)

    def to_dict(self):
        return {"true_utility": [self.true_utility],
                "perc_utility": [self.perc_utility],
                "num_selected_x_cands": [self.num_selected_x_cands],
                "sp_entry_id": [self.sp_entry_id]}


class QueuedHitParams(models.Model):
    n_x = models.IntegerField(default=50)
    n_y = models.IntegerField(default=50)
    k = models.IntegerField(default=10)
    l = models.IntegerField(default=0)
    bias = models.FloatField(default=0.75)
    n_iterations = models.IntegerField(default=0)
    pts_per_dollar = models.IntegerField(default=15000)
    base_reward = models.TextField(default=f"{1.00:0.2f}")
    avg_bonus_reward = models.TextField(default=f"{1.00:0.2f}")
    avg_n_minutes_to_complete = models.IntegerField(default=20)
    using_sandbox = models.BooleanField(default=True)

class InProgressHits(models.Model):
    assignment_id = models.TextField(primary_key=True)
    worker_id = models.TextField()
    hit_id = models.TextField()
    n_iterations = models.IntegerField()
    n_x = models.IntegerField()
    n_y = models.IntegerField()
    k = models.IntegerField()
    l = models.IntegerField()
    bias = models.FloatField()
    start_time = models.BigIntegerField() # In milliseconds since start of 1970
    last_update_time = models.BigIntegerField()
    selected = models.TextField(default="[]") # JSON array of selected so far
    db_entry_id = models.TextField(default="[]") # JSON array of db_entry_ids so far
    round_completion_time = models.TextField(default="[]") # JSON array of round_completion_times so far
    true_utility = models.TextField(default="[]") # JSON array of db_entry_ids so far
    base_reward = models.FloatField()
    avg_bonus_reward = models.FloatField()
    avg_n_minutes_to_complete = models.IntegerField()
    pts_per_dollar = models.IntegerField()


