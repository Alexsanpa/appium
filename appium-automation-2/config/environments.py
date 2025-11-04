# config/environments.py
"""
Gestor de configuraciones por entorno
Permite tener diferentes configuraciones para dev, qa, staging, prod
"""
import os
from pathlib import Path
from typing import Literal

EnvType = Literal['dev', 'qa', 'staging', 'prod']


class EnvironmentConfig:
    """Configuraciones específicas por entorno"""
    
    CONFIGS = {
        'dev': {
            'DEVICE_NAME': 'emulator-5554',
            'DEVICE_PLATFORM_VERSION': '16',
            'APP_INSTALL': False,
            'EVIDENCE_VIDEO_ENABLED': True,
            'EVIDENCE_GENERATE_HTML': True,
            'EVIDENCE_GENERATE_PDF': True,
            'TEST_MAX_RETRIES': 0,
            'TEST_VERBOSE': True,
        },
        'qa': {
            'DEVICE_NAME': 'emulator-5554',
            'DEVICE_PLATFORM_VERSION': '16',
            'APP_INSTALL': True,  # En QA siempre instalar APK limpio
            'EVIDENCE_VIDEO_ENABLED': True,
            'EVIDENCE_GENERATE_HTML': True,
            'EVIDENCE_GENERATE_PDF': True,
            'TEST_MAX_RETRIES': 1,  # Reintentar tests fallidos
            'TEST_VERBOSE': False,
        },
        'staging': {
            'DEVICE_NAME': 'device-real-001',  # Dispositivo físico
            'DEVICE_PLATFORM_VERSION': '14',
            'APP_INSTALL': True,
            'EVIDENCE_VIDEO_ENABLED': True,
            'EVIDENCE_GENERATE_HTML': True,
            'EVIDENCE_GENERATE_PDF': True,
            'TEST_MAX_RETRIES': 2,
            'TEST_VERBOSE': False,
        },
        'prod': {
            'DEVICE_NAME': 'device-real-001',
            'DEVICE_PLATFORM_VERSION': '14',
            'APP_INSTALL': False,  # En prod usar app ya instalada
            'EVIDENCE_VIDEO_ENABLED': True,
            'EVIDENCE_GENERATE_HTML': True,
            'EVIDENCE_GENERATE_PDF': True,
            'TEST_MAX_RETRIES': 3,  # Más reintentos en prod
            'TEST_VERBOSE': False,
        }
    }
    
    @classmethod
    def get_env_config(cls, env: EnvType) -> dict:
        """
        Obtiene la configuración para un entorno específico
        
        Args:
            env: Entorno (dev, qa, staging, prod)
            
        Returns:
            dict: Configuración del entorno
        """
        return cls.CONFIGS.get(env, cls.CONFIGS['dev'])
    
    @classmethod
    def apply_env_config(cls, env: EnvType):
        """
        Aplica la configuración de un entorno específico a las variables de entorno
        
        Args:
            env: Entorno a aplicar
        """
        config = cls.get_env_config(env)
        
        print(f"\n🌍 Aplicando configuración del entorno: {env.upper()}")
        print("="*60)
        
        for key, value in config.items():
            os.environ[key] = str(value)
            print(f"  ✓ {key} = {value}")
        
        print("="*60 + "\n")


def load_env_file(env: EnvType = 'dev'):
    """
    Carga un archivo .env específico según el entorno
    
    Archivos soportados:
    - .env.dev
    - .env.qa
    - .env.staging
    - .env.prod
    - .env (fallback)
    
    Args:
        env: Entorno a cargar
    """
    from dotenv import load_dotenv
    
    base_dir = Path(__file__).resolve().parent.parent
    env_file = base_dir / f'.env.{env}'
    
    if env_file.exists():
        load_dotenv(env_file, override=True)
        print(f"✅ Configuración cargada desde: .env.{env}")
    else:
        fallback = base_dir / '.env'
        if fallback.exists():
            load_dotenv(fallback)
            print(f"⚠️ Archivo .env.{env} no encontrado, usando .env")
            # Aplicar overrides del entorno
            EnvironmentConfig.apply_env_config(env)
        else:
            print(f"⚠️ No se encontró archivo .env, usando valores por defecto")
            EnvironmentConfig.apply_env_config(env)


# Función helper para cambiar de entorno en tiempo de ejecución
def switch_environment(env: EnvType):
    """
    Cambia el entorno actual
    
    Args:
        env: Nuevo entorno (dev, qa, staging, prod)
    """
    os.environ['TEST_ENVIRONMENT'] = env
    load_env_file(env)
    
    # Recargar la configuración
    from config import settings
    import importlib
    importlib.reload(settings)
    
    print(f"🔄 Entorno cambiado a: {env.upper()}")


if __name__ == "__main__":
    # Ejemplo de uso
    print("Probando configuraciones por entorno:\n")
    
    for env in ['dev', 'qa', 'staging', 'prod']:
        config = EnvironmentConfig.get_env_config(env)
        print(f"\n{'='*60}")
        print(f"Entorno: {env.upper()}")
        print(f"{'='*60}")
        for key, value in config.items():
            print(f"  {key}: {value}")