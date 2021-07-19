import { Entry, EntryCollection } from 'contentful';
import { Route } from 'vue-router';
import VueRouter from 'vue-router'


export interface Resource {
  description: string;
  name: string;
  owner: string;
  resourceType: ResourceType
  url: string;
  logo?: Entry<Logo>
}

export interface Data {
  title: string;
  breadcrumb: Breadcrumb[]
  resourceData: EntryCollection<Resource>;
  tabTypes: TabType[];
  isLoadingSearch: boolean;
  activeTab: string;
}

export interface Computed {
  currentResourceCount: number;
  tableData: any[];
  curSearchPage: number;
  resourceHeading: string;
}

export interface Methods {
  updateDataSearchLimit: (this: ResourcesComponent, limit: number | string) => void;
  fetchResults: (this: ResourcesComponent) => void;
  onPaginationPageChange: (this: ResourcesComponent, page: number) => void;
  setActiveTab: (this: ResourcesComponent, tab: string) => void;
}

export type ResourcesComponent = Data & Computed & Methods & { $route: Route, $router: VueRouter }


type ResourceType = 'Device' | 'Information Services' | 'Databases' | 'Software' | 'Biologicals' | 'sparcPartners'

interface TabType {
  label: string,
  type: ResourceType,
}

// supporting types that might belong in a more general place

interface Breadcrumb {
  to: {
    name: string;
  };
  label: string;
}

interface File {
  contentType: string;
  fileName: string;
  details: {
    size: number;
    image: {
      height: number;
      width: number;
    }
  }
}

interface Logo {
  description: string;
  title: string;
  file: File;
}
