<template>
  <div
    class="dropdown is-right"
    @click="showCasesMenu = !showCasesMenu; "
    v-bind:class="{ 'is-active': showCasesMenu }"
  >
    <div class="dropdown-trigger">
      <button>
        <i class="far fa-ellipsis-v"></i>
      </button>
    </div>
    <div class="dropdown-menu" id="dropdown-menu" role="menu">
      <div class="dropdown-content">
        <a
          class="dropdown-item"
          @click="
            showAttachCasesModal = !showAttachCasesModal;
            filterCases();">attach cases</a>
        <a class="dropdown-item">
          detach cases
        </a>
        <hr class="dropdown-divider" />
        <a href="#" class="dropdown-item">
          delete
        </a>
      </div>
    </div>
  </div>

  <div v-bind:class="{ 'is-active': showAttachCasesModal }" class="modal">
    <div class="modal-background"></div>
    <div class="modal-card">
      <!-- <header class="modal-card-head">
        <p class="modal-card-title">Select target case</p>
        <button class="delete" aria-label="close" @click="showAttachCasesModal = false"></button>
      </header> -->

      <section class="modal-card-body">
        <div class="title">select the target case</div>
        <table
          class="table is-fullwidth is-striped is-clickable"
          v-if="casesSelected.length > 0"
        >
          <tbody>
            <tr
              v-for="item in casesToDisplay"
              :key="item.id"
              @click="attachCasesTo(item.id)"
            >
              <td>
                {{ item.name }}
              </td>
            </tr>
          </tbody>
        </table>
        <div v-if="casesSelected.length == 0 || casesToDisplay.length == 0">
          No data to display. Perhaps you select all cases or maybe no case at
          all?
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
        <button class="button" @click="showAttachCasesModal = false">
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
      error: null,
      showAttachCasesModal: false,
      showCasesMenu: false,
      casesToDisplay: []
    };
  },
  props: {
    casesSelected: Array,
    cases: Array,
    projectId: String
  },
  methods: {
    attachCasesTo(parent_id) {
      const payload = {
        cases_array: this.casesSelected,
        parent_id: parent_id,
        project_id: this.projectId
      };
      const requestOptions = {
        method: "post",
        url: "/cases/attach",
        data: payload
      };
      axios(requestOptions)
        .then(response => {
          // TODO: add visual feedback that is working`
          if (response.data.message != "CASE_CREATED") {
            this.error = response.data.message;
          } else {
            this.showAttachCasesModal = false;
            this.newCase = "";
          }
        })
        .catch(error => {
          this.error = error;
        });
    },
    filterCases() {
      this.error = "";
      this.casesToDisplay = this.cases.filter(
        d => !this.casesSelected.includes(d)
      );
    }
  }
};
</script>
