<template>
  <router-link class="dashboard_item_link" :to="{ name: 'projectDashboard', params: { projectId: project_details.id }}">
    <div class="dashboard_item dashboard_default">
      <p style="font-size: 7px">project name:</p>
      <p class="title dashboard_title">{{ project_details.name }}</p>
      <p style="font-size: 7px">description:</p>
      <p class="is-text-overflow" style="font-weight: 500;">
        {{ project_details.description }}</p>
      <br />
      <div v-if="project_details.have_cycle">
        <p style="font-size: 7px;">
          current cycle summary:
        </p>
        <p style="font-size: 20px">Cycle number 35</p>
        <div class="column">
          <div
            :class="charist_random_class"
            style="height: 20px; margin-left: -59px;"
          ></div>
          <br />
        </div>
        <div class="columns">
          <div class="column" style="font-size: 9px">
            passed: {{ project_details.stats.total_passed }}
          </div>
          <div class="column" style="font-size: 9px">
            failed: {{ project_details.stats.total_error }}
          </div>
          <div class="column" style="font-size: 9px">
            blocked: {{ project_details.stats.total_blocked }}
          </div>
          <div class="column" style="font-size: 9px">
            not executed: {{ project_details.stats.total_not_executed }}
          </div>
        </div>
      </div>
      <div v-else style="text-align: center">
        <i class="fal fa-pie" style="font-size: 50px"></i>
        <p style="font-family: Nunito">
          Hey, brand new project! Have some pie ;)
        </p>
        <p></p>
      </div>
    </div>
  </router-link>
</template>

<script>
import Chartist from "chartist";
require("chartist-plugin-legend");

export default {
  props: ["project"],
  data() {
    return {
      project_details: this.project,
      have_cycle: true,
      charist_random_class: "project_chartist_" + this._.uid
    };
  },
  methods: {
    chartist() {
      Chartist.Bar(
        "." + this.charist_random_class,
        {
          series: [
            [this.project_details.stats.total_passed],
            [this.project_details.stats.total_error],
            [this.project_details.stats.total_blocked],
            [this.project_details.stats.total_not_executed]
          ]
        },
        {
          stackBars: true,
          horizontalBars: true
        }
      ).on("draw", function(data) {
        if (data.type === "bar") {
          data.element.attr({
            style: "stroke-width: 20px"
          });
        }
      });
    }
  },
  mounted() {
    if (this.project_details.have_cycle) {
      this.chartist();
    }
  }
};
</script>
<style>
.dashboard_item {
  color: black !important;
  opacity: 0.8;
  transition: 0.3s;
}

.dashboard_item:hover {
  color: #615d5d;
  border: 1px solid;
  opacity: 1;
}

.dashboard_item:hover {
  color: #615d5d;
  border: 1px solid;
}

html {
  background-color: #eff1f3 !important;

  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
