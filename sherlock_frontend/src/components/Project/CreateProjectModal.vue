<template>
  <a class="navbar-item" @click="showCreateProjectModal = true">
    Create Project
  </a>
  <div v-bind:class="{ 'is-active': showCreateProjectModal }" class="modal">
    <div class="modal-background"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Create Project</p>
        <button class="delete" aria-label="close" @click="showCreateProjectModal = false"></button>
      </header>
      <section class="modal-card-body">
        <div class="field">
          <div class="control">
            <input
              class="input"
              type="text"
              placeholder="project name"
              style="width:50%"
              id="newProjectName"
              v-model="registerProject.name"
            />
          </div>
        </div>
        <div class="field">
          <div class="control has-icons-left has-icons-right">
            <textarea
              class="textarea"
              placeholder="project description"
              style="width:50%"
              id="newProjectDescription"
              v-model="registerProject.description"
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
        <button class="button is-primary" @click="createProject()">create</button>
        <button class="button" @click="showCreateProjectModal = false">cancel</button>
      </footer>
    </div>
  </div>
</template>
<script>
import axios from "axios";

export default {
  data() {
    return {
      showCreateProjectModal: false,
      registerProject: {
        name: null,
        description: null,
      },
      error: null
    }
  },
  methods: {
    createProject: function() {
      if (
        !this.registerProject.name ||
        !this.registerProject.description
      ) {
        this.error = "Please fill all the inputs to create a project";
        return false;
      }
      var requestOptions = {
        method: "post",
        url: "/projects/new",
        data: {
          name: this.registerProject.name,
          description: this.registerProject.description
        }
      };
      axios(requestOptions)
        .then(response => {
          // TODO: add visual feedback that is working
          if (response.data.message != "PROJECT_CREATED") {
            this.error = response.data.message;
          } else {
            this.showCreateProjectModal = false;
            this.$router.push({ name: 'projectDashboard', params: { projectId: response.data.project_id }});
          }
        })
        .catch(error => {
          this.error = error;
        });
    },
  }
};
</script>
