import { mount, shallowMount } from '@vue/test-utils'
import Sidebar from '@/components/Sidebar.vue'

import CreateProjectForm from '@/components/CreateProjectForm.vue'
import { BButton, BDropdown, BModal, BDropdownItem, BRow, BCol } from 'bootstrap-vue'


const authMock = {
    user: {
        user_id: 1
    }, 
    loggedIn: true, 
    strategy: {
        token: {
            get: () => 'token'
        }
    }
};

const projects = [
    {
        "project_id": 0,
        "project_name": "a",
        "recent_evaluation_label": "Successful",
        "project_manager_name": "a"
    },
    {
        "project_id": 1,
        "project_name": "b",
        "recent_evaluation_label": "Failing",
        "project_manager_name": "b"
    },
    {
        "project_id": 2,
        "project_name": "c",
        "recent_evaluation_label": "Showing Symptoms",
        "project_manager_name": "c"
    }
];

describe('Sidebar', () => {
    

    let wrapper; 
    beforeEach(() => {
        wrapper = shallowMount(Sidebar, {
            stubs: {
                'b-modal' : BModal,
                'b-button' : BButton,
                'b-dropdown' : BDropdown,
                'b-dropdown-item' : BDropdownItem,
                'b-row' : BRow,
                'b-col' : BCol,
                'CreateProjectForm' : CreateProjectForm
            }, 
            mocks: {
                $auth: authMock
            },
            propsData: {
                projects : projects
            }
        })
    })

    it('should not be null', () => {
        const project = { projectID: 1, project_name: 'Project Mbappe', recent_evaluation_label: 'Failing', project_manager_name: 'John Doe'}
        wrapper.vm.handleProjectCreated(project)
        expect(wrapper.vm.$props.projects).not.toBeNull()
    })

    it('should not be undefined', () => {
        const project = { projectID: 1, project_name: 'Project Mbappe', recent_evaluation_label: 'Failing', project_manager_name: 'John Doe'}
        wrapper.vm.handleProjectCreated(project)
        expect(wrapper.vm.$props.projects).not.toBeUndefined()
    })

    it('showCreateProjectModal should be false', () => {
        expect(wrapper.vm.$data.showCreateProjectModal).toBeFalsy()
    })
})