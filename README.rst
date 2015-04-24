===================
Requirements parser
===================

Menu:
=====
* `How to preconfigure your system`_
* How to use this parser
    - `Without config`_
    - `With config`_

How to preconfigure your system
-------------------------------

* This tool used ``colorama``, run ``pip install colorama rst2pdf rst2html5``

* On the Debian-based (Debian, Ubuntu and other) run ``apt-get install -y mailutils aptitude``
* On the RHEL-based (Fedora, CentOS and other) run ``yum install -y mailutils``
  (migrate option not available for this distribution)

* You should to select ``Internet site`` button

If you use 'migrate' option
^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Create *.list file in ``/etc/apt/sources.list.d/{your_list}`` with content: 
    ``deb  {mirantis_repo} {version} main``

* Create *.pin file in ``/etc/apt/preferences.d/{your_file}`` with content:
    ``Package: *``
    
    ``Pin: release o=Mirantis``
    
    ``Pin-Priority: 1000``

How to use this parser
----------------------
Without config
^^^^^^^^^^^^^^
You can store you repo list in file, named ``repos_name``.
Just make ``python main.py``,  and answer on the questions.
  
With config
^^^^^^^^^^^
You must use yaml-file. In this yaml:
  * Launchpad ID (Parameter: ``launchpad_id``);
  * Launchpad password (Parameter: ``launchpad_pw``);
  * Mode (Parameter: ``mode``; values: ``req``, ``ep``, ``diff``, ``migr``):
    
    - If mode ``req``:
      
      + Should we use data, stored in a spec or control file? 
        
        * Parameter: ``type_req``; 
        * Values: ``''``, ``'control'``, ``'spec'``;
        
      + Branch name 
        
        * Parameter: ``branch``;
        * Values: ``master``, ``6.1``, ``6.0.1``;
        
      + Global branch name
        
        * Parameter: ``global_branch``;
        * Value: ``master``, ``kilo``, ``juno``, ``icehouse``;
        
    - If mode ``ep``:
      
      + Should we use data, stored in a spec or control file? 
        
        * Parameter: ``type_req``; 
        * Values: ``''``, ``'control'``, ``'spec'``;
        
      + Branch name 
        
        * Parameter: ``branch``;
        * Values: ``master``, ``6.1``, ``6.0.1``;
    - If mode ``migr``:
    
      + Global branch name
        
        * Parameter: ``global_branch``;
        * Value: ``master``, ``kilo``, ``juno``, ``icehouse``;
  
  * Output format:
  
    - Parameter: ``output_format``; Values: ``pdf``, ``html``;
    - If you use ``migr`` mode option, ``output_format`` option not used
    
  * Would you like to send report via email? 
    
    - Parameter: ``send_email``; Values: ``yes``, ``no``;
    - If ``yes``:
      
      + Specify the email;
      
After creating your yaml-file you should make ``python main.py -c {config}.yaml``, where you specify your config.
You can store you repo list in file, named ``repos_name``. 
If tool not found file named ``repos_name``, it will ask you, in which file stored repo list.
