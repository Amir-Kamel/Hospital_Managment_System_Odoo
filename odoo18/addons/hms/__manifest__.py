
{
    'name': "hms",

    'description': """
Patients information management system
    """,



    'data': [
        'views/patient_views.xml',
        'views/doctor_views.xml',
        'views/department_views.xml',
        'views/related_patient_views.xml',
        'views/patient_status_report.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
    ],

    'depends': ['base', 'contacts', 'crm'],

}

