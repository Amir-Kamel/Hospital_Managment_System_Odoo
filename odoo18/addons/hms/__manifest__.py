
{
    'name': "hms",

    'description': """
Patients information management system
    """,



    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/patient_views.xml',
        'views/doctor_views.xml',
        'views/department_views.xml',
        'views/related_patient_views.xml',
    ],

    'depends': ['base', 'contacts', 'crm'],

}

