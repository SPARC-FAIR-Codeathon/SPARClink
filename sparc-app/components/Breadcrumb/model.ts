import { Location } from 'vue-router/types/router'

export interface Breadcrumb {
  to: Location;
  label: string
}

export interface Props {
  breadcrumb: Breadcrumb[]
  title: string
}
export interface Methods {
  formatTitle: (title: string) => string
}
