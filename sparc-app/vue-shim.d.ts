import Vue, { ComponentOptions } from 'vue';
import { Store } from 'vuex';
import { Route } from 'vue-router';

declare module "*.vue" {
  export default Vue
}

declare module "vue/types/options" {
  interface ComponentOptions<V extends Vue, Data> {
    asyncData?: (store: Store<any>, route: Route) => Promise<Partial<Data> | void>;
  }
}

declare module "vue/types/vue" {
  interface Vue<Data> {
    asyncData?: (store: Store<any>, route: Route) => Promise<Partial<Data> | void>;
  }
}
