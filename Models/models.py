from .Base.models_base import Base as Base_base
from .LifeCycles.models_lifeCycle import Base as Base_conf_lc
from .Core.models_core import Base as Base_core
from .Refbooks.models_refbook import Base as Base_refbook
from .models_Abstract import Base_ABS

target_metadata_main = [ 
                    Base_ABS.metadata ,
                    Base_refbook.metadata ,
                    Base_conf_lc.metadata ,
                    Base_base.metadata ,
                    #Base_core.metadata 
                    ]



