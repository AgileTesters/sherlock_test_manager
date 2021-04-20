<template>
  <p class="panel-heading sherlock_tiles">
    actions menu
  </p>
  <router-link
    class="panel-block"
    :to="{ name: 'manageCases', params: { projectId: project.id } }"
  >
    <span class="panel-icon">
      <i class="fas fa-book" aria-hidden="true"></i>
    </span>
    manage cases
  </router-link>

  <div v-if="project.last_cycle.cycle || project.last_cycle.closed">
    <a class="panel-block" @click="executeCase()">
      <span class="panel-icon">
        <i class="fas fa-code-branch" aria-hidden="true"></i>
      </span>
      execute test
    </a>
    <a class="panel-block">
      <span class="panel-icon">
        <i class="fas fa-code-branch" aria-hidden="true"></i>
      </span>
      stop cycle
    </a>
  </div>
  <div v-else>
    <div v-if="project.qty_cases > 0">
      <a class="panel-block" @click="showCreateCycleModel = true">
        <span class="panel-icon">
          <i class="fas fa-code-branch" aria-hidden="true"></i>
        </span>
        new execution cycle
      </a>
    </div>
  </div>

  <div v-bind:class="{ 'is-active': showCreateCycleModel }" class="modal">
    <div class="modal-background"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Create Cycle</p>
        <button
          class="delete"
          aria-label="close"
          @click="showCreateCycleModel = false"
        ></button>
      </header>
      <section class="modal-card-body">
        <div class="field">
          <div class="control">
            <input
              class="input"
              type="text"
              placeholder="Cycle name"
              style="width:50%"
              v-model="newCycle.name"
            />
          </div>
        </div>
        <div class="field is-grouped">
          <div class="control">
            <p v-if="error" id="login_display_msg" class="help is-danger">
              {{ error }}
            </p>
          </div>
        </div>
      </section>
      <footer class="modal-card-foot">
        <button class="button is-primary" @click="createCycle()">create</button>
        <button class="button" @click="showCreateCycleModel = false">
          cancel
        </button>
      </footer>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      showCreateCycleModel: false,
      error: false,
      newCycle: {
        cycle_name: "",
        project_id: this.$route.params.projectId
      }
    };
  },
  props: {
    project: Object
  },
  methods: {
    executeCase: function() {
      this.$router.push({
        name: "executeCases",
        params: { projectId: this.$route.params.projectId }
      });
    },
    createCycle: function() {
      if (this.project.last_cycle.cycle || this.project.last_cycle.closed) {
        this.error =
          "Cannot create a new cycle when the previous one still active";
        return false;
      }

      if (this.project.qty_cases == 0) {
        this.error = "Cannot create a new cycle when there is no case created";
        return false;
      }
      var requestOptions = {
        method: "post",
        url: "/cycles/new",
        data: {
          cycle_name: this.newCycle.cycle_name,
          project_id: this.newCycle.project_id
        }
      };

      axios(requestOptions)
        .then(response => {
          // TODO: add visual feedback that is working
          if (response.data.message != "CYCLE_CREATED") {
            this.error = response.data.message;
          } else {
            this.showCreateCycleModel = false;
            this.$router.push({
              name: "executeCases",
              params: { projectId: this.$route.params.projectId }
            });
          }
        })
        .catch(error => {
          this.error = error.response.data.message;
        });
    }
  }
};
</script>
