<template>
  <div class="citation-details">
    <div class="citation-details__container">
      <h3>Cite This Dataset</h3>
      <p>
        Publication Date: {{ publishedDate }}<br />
        Platform:
        <a href="https://discover.blackfynn.com/" target="_blank">
          Pennsieve Discover
        </a>
      </p>
      <div id="citationsArea" class="citation-details__container--citation">
        <el-row type="flex" justify="center">
          <el-col :span="24">
            <ul class="citation-details__container--citation-links">
              <li
                v-for="citationType in citationTypes"
                :key="citationType.type"
              >
                <a
                  :title="citationTypeTitle(citationType)"
                  :class="{
                    'active-citation': activeCitation.type === citationType.type
                  }"
                  @click="handleCitationChanged(citationType)"
                >
                  {{ citationType.label }}
                </a>
              </li>
              <li>
                <a
                  :href="`https://citation.crosscite.org/?doi=${doiValue}`"
                  target="_blank"
                >
                  More on Crosscite.org
                </a>
              </li>
            </ul>
            <div
              v-show="!hasCitationError"
              v-loading="citationLoading"
              class="info-citation"
              aria-live="polite"
              v-html="citationText"
            />
            <div v-show="hasCitationError">
              <p>
                <strong>Internal Server Error</strong><br />
                Sorry, something went wrong.<br />
                The dataset citation generator (<a
                  href="https://citation.crosscite.org/"
                  target="_blank"
                >https://citation.crosscite.org/</a>) encountered an internal error and was unable to complete your
                request.<br />
                Please come back later.
              </p>
            </div>
            <el-button
              :disabled="hasCitationError"
              class="copy-button"
              size="small"
              @click="handleCitationCopy"
            >
              Copy Citation
            </el-button>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
import { successMessage, failMessage } from '@/utils/notification-messages'

export default {
  name: 'CitationDetails',
  props: {
    publishedDate: {
      type: String,
      default: ''
    },

    doiValue: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      citationLoading: false,
      citationText: '',
      activeCitation: '',
      crosscite_host: process.env.crosscite_api_host,
      hasCitationError: false,
      citationTypes: [
        {
          type: 'apa',
          label: 'APA'
        },
        {
          type: 'chicago-note-bibliography',
          label: 'Chicago'
        },
        {
          type: 'ieee',
          label: 'IEEE'
        },
        {
          type: 'bibtex',
          label: 'Bibtex'
        }
      ]
    }
  },
  watch: {
    doiValue: {
      handler: function(val) {
        if (val) {
          const initialCitationType = this.citationTypes.filter(
            citationType => {
              return citationType.type == 'apa'
            }
          )[0]
          this.handleCitationChanged(initialCitationType)
        }
      },
      immediate: true
    }
  },
  methods: {
    /**
     * gets bibiolography based on citation type for current DOI
     * @param {String} citationType
     */
    handleCitationChanged: function(citationType) {
      if (citationType === this.activeCitation) {
        return
      }
      this.citationLoading = true
      this.hasCitationError = false
      this.activeCitation = citationType
      // find all citation types at https://github.com/citation-style-language/style
      const url = `${this.crosscite_host}/format?doi=${this.doiValue}&style=${citationType.type}&lang=en-US`
      fetch(url)
        .then(response => {
          if (response.status !== 200) {
            throw Error
          }
          return response.text()
        })
        .then(text => {
          this.citationText = text
        })
        .catch(() => {
          this.hasCitationError = true
        })
        .finally(() => {
          this.citationLoading = false
        })
    },

    /**
     * Handle copy citation to clipboard
     */
    handleCitationCopy: function() {
      this.$copyText(this.citationText).then(() => {
        this.$message(
          successMessage(
            `${this.activeCitation.label} citation copied to clipboard.`
          )
        )
      }),
        () => {
          this.$message(failMessage('Failed to copy citation.'))
        }
    },

    /**
     * Title for citation type while hovering over link
     * @param {Object} citationType
     * @returns {String}
     */
    citationTypeTitle: function(citationType) {
      return `Format citation ${citationType.label}`
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/_variables.scss';
.citation-details {
  &__container {
    background: white;
    border: solid 1px $cloudy;
    padding: 2em;
    margin: 1.25rem 0 2rem;

    h3 {
      font-size: 0.875em;
      font-weight: 500;
      line-height: 1em;
      color: black;
    }

    p {
      font-size: 0.875em;
      font-weight: normal;
      line-height: 24px;
      color: black;
    }

    &--citation {
      height: 100%;
      background: $washed-gray;
      padding-left: 1rem;
      padding-right: 1rem;
      margin-bottom: 1.5rem;
      .copy-button {
        margin: 1.875rem 0 1rem 0;
        background: #f9f2fc;
        border: 1px solid $median;
        cursor: pointer;
        color: $median;
        &:hover {
          color: #1a1489;
        }
      }
    }

    .info-citation {
      font-size: 14px;
      font-weight: normal;
      line-height: 24px;
      color: black;
      margin-top: 1rem;
    }

    &--citation-links {
      border-bottom: 1px solid #e4e7ed;
      display: flex;
      flex-wrap: wrap;
      list-style: none;
      padding: 0;
      li {
        margin-right: 0.5rem;
        :hover {
          border-bottom: 2px solid $median;
          padding-bottom: 0.094rem;
        }
        a {
          color: black;
          text-decoration: none;
          padding: 0 0.5rem;
          cursor: pointer;
          &.active-citation {
            color: $median;
            border-bottom: 2px solid $median;
            padding-bottom: 0.094rem;
          }
        }
      }
    }

    &--protocol-text {
      color: black;
      text-decoration: none;
      font-size: 0.875em;
      line-height: 24px;
      font-weight: normal;
    }

    &--protocol-text-na {
      p {
        margin-bottom: 0;
      }
    }

    .protocol-block {
      margin-bottom: 1rem;
    }
  }
}
</style>
