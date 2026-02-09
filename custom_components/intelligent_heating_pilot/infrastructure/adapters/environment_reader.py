"""Home Assistant environment reader adapter.

Reads environmental state from Home Assistant entities (temperatures, humidity, etc.)
and converts them to domain value objects.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING

from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

from ...domain.value_objects import EnvironmentState
from ...const import VTHERM_ATTR_MAX_CAPACITY_HEAT
from ..vtherm_compat import get_vtherm_attribute
from .utils import get_entity_name

if TYPE_CHECKING:
    pass

_LOGGER = logging.getLogger(__name__)


class HAEnvironmentReader:
    """Reads environmental conditions from Home Assistant entities.
    
    Converts HA entity states into domain EnvironmentState value objects.
    No business logic - pure data translation.
    """
    
    def __init__(
        self,
        hass: HomeAssistant,
        vtherm_entity_id: str,
        outdoor_temp_entity_id: str | None = None,
        humidity_in_entity_id: str | None = None,
        humidity_out_entity_id: str | None = None,
        cloud_cover_entity_id: str | None = None,
        vtherm_auto_tpi_sensor_entity_id: str | None = None,
    ) -> None:
        """Initialize the environment reader.
        
        Args:
            hass: Home Assistant instance
            vtherm_entity_id: VTherm climate entity ID
            outdoor_temp_entity_id: Outdoor temperature sensor (optional)
            humidity_in_entity_id: Indoor humidity sensor (optional)
            humidity_out_entity_id: Outdoor humidity sensor (optional)
            cloud_cover_entity_id: Cloud coverage sensor (optional)
            vtherm_auto_tpi_sensor_entity_id: Auto TPI sensor entity ID (optional, for Heat Rate)
        """
        self._hass = hass
        self._vtherm_entity_id = vtherm_entity_id
        self._outdoor_temp_entity_id = outdoor_temp_entity_id
        self._humidity_in_entity_id = humidity_in_entity_id
        self._humidity_out_entity_id = humidity_out_entity_id
        self._cloud_cover_entity_id = cloud_cover_entity_id
        self._vtherm_auto_tpi_sensor_entity_id = vtherm_auto_tpi_sensor_entity_id
        self._device_name = get_entity_name(hass, vtherm_entity_id)
    
    async def get_current_environment(self) -> EnvironmentState | None:
        """Read current environmental state from HA entities.
        
        Returns:
            EnvironmentState value object, or None if required data missing
        """
        # Get current indoor temperature from VTherm
        vtherm_state = self._hass.states.get(self._vtherm_entity_id)
        if not vtherm_state:
            _LOGGER.warning("[%s] VTherm entity not found", self._device_name)
            return None
        
        # Use v8.0.0+ compatible attribute access
        current_temp_raw = get_vtherm_attribute(vtherm_state, "current_temperature")
        if current_temp_raw is None:
            _LOGGER.warning("[%s] No current_temperature available", self._device_name)
            return None
        
        try:
            current_temp = float(current_temp_raw)
        except (ValueError, TypeError):
            _LOGGER.warning("Invalid current_temperature: %s", current_temp_raw)
            return None
        
        # Get outdoor temperature (required for EnvironmentState)
        outdoor_temp = self._get_float_state(self._outdoor_temp_entity_id)
        if outdoor_temp is None:
            # Fallback: use current temp if outdoor not available
            outdoor_temp = current_temp
            _LOGGER.debug("No outdoor temp available, using indoor temp as fallback")
        
        # Get humidity (required for EnvironmentState)
        humidity = self._get_float_state(self._humidity_in_entity_id)
        if humidity is None:
            # Default fallback humidity
            humidity = 50.0
            _LOGGER.debug("No indoor humidity available, using default 50%%")
        
        # Optional sensors
        outdoor_humidity = self._get_float_state(self._humidity_out_entity_id)
        cloud_coverage = self._get_float_state(self._cloud_cover_entity_id)
        
        return EnvironmentState(
            indoor_temperature=current_temp,
            outdoor_temp=outdoor_temp,
            indoor_humidity=humidity,
            timestamp=dt_util.now(),
            outdoor_humidity=outdoor_humidity,
            cloud_coverage=cloud_coverage,
        )
    
    def get_vtherm_slope(self) -> float | None:
        """Get current heating slope from VTherm.
        
        Returns:
            Current slope in °C/h, or None if not available
        """
        vtherm_state = self._hass.states.get(self._vtherm_entity_id)
        if not vtherm_state:
            return None
        
        # Use v8.0.0+ compatible attribute access
        slope_raw = get_vtherm_attribute(vtherm_state, "slope")
        if slope_raw is None:
            return None
        
        try:
            return float(slope_raw)
        except (ValueError, TypeError):
            return None
    
    def get_vtherm_heat_rate(self) -> float | None:
        """Get Heat Rate from VTherm's auto TPI.
        
        Reads the max_capacity_heat attribute which represents the Heat Rate
        calculated by Versatile Thermostat's auto TPI algorithm.
        
        The attribute is exposed on the Auto TPI sensor entity (not the climate
        entity). Uses configured sensor entity if provided, otherwise attempts
        auto-discovery.
        
        Returns:
            Heat Rate in °C/h, or None if not available
        """
        # Priority 1: Use configured sensor entity if provided
        if self._vtherm_auto_tpi_sensor_entity_id:
            sensor_state = self._hass.states.get(self._vtherm_auto_tpi_sensor_entity_id)
            if sensor_state and sensor_state.attributes:
                heat_rate_raw = sensor_state.attributes.get(VTHERM_ATTR_MAX_CAPACITY_HEAT)
                if heat_rate_raw is not None:
                    try:
                        heat_rate = float(heat_rate_raw)
                        if heat_rate > 0:
                            _LOGGER.debug(
                                "[%s] Found Heat Rate %.3f°C/h from configured sensor %s",
                                self._device_name,
                                heat_rate,
                                self._vtherm_auto_tpi_sensor_entity_id
                            )
                            return heat_rate
                    except (ValueError, TypeError) as e:
                        _LOGGER.debug(
                            "[%s] Invalid Heat Rate value from configured sensor %s: %s",
                            self._device_name,
                            self._vtherm_auto_tpi_sensor_entity_id,
                            heat_rate_raw,
                            exc_info=e
                        )
            else:
                _LOGGER.warning(
                    "[%s] Configured Auto TPI sensor entity %s not found",
                    self._device_name,
                    self._vtherm_auto_tpi_sensor_entity_id
                )
        
        # Priority 2: Try auto-discovery (if not configured or configured entity failed)
        # Sensor entity ID pattern: {climate_entity_id}_auto_tpi_learning
        # e.g., climate.office_heater -> sensor.office_heater_auto_tpi_learning
        climate_domain, climate_entity = self._vtherm_entity_id.split(".", 1)
        
        # Try multiple possible entity ID patterns
        possible_sensor_ids = [
            f"sensor.{climate_entity}_auto_tpi_learning",
            f"sensor.{climate_entity.replace('_', '')}_auto_tpi_learning",  # Without underscores
        ]
        
        # Also search all sensor entities for one with matching unique_id pattern
        # The unique_id is {device_name}_auto_tpi_learning, but entity_id might differ
        for sensor_entity_id in possible_sensor_ids:
            sensor_state = self._hass.states.get(sensor_entity_id)
            if sensor_state and sensor_state.attributes:
                heat_rate_raw = sensor_state.attributes.get(VTHERM_ATTR_MAX_CAPACITY_HEAT)
                if heat_rate_raw is not None:
                    try:
                        heat_rate = float(heat_rate_raw)
                        if heat_rate > 0:
                            _LOGGER.debug(
                                "[%s] Found Heat Rate %.3f°C/h from sensor %s",
                                self._device_name,
                                heat_rate,
                                sensor_entity_id
                            )
                            return heat_rate
                    except (ValueError, TypeError) as e:
                        _LOGGER.debug(
                            "[%s] Invalid Heat Rate value from sensor %s: %s",
                            self._device_name,
                            sensor_entity_id,
                            heat_rate_raw,
                            exc_info=e
                        )
        
        # Search all sensor entities for one with max_capacity_heat attribute
        # that might belong to this VTherm device (fallback if entity ID pattern doesn't match)
        vtherm_state = self._hass.states.get(self._vtherm_entity_id)
        if vtherm_state:
            # Get device_id from climate entity if available
            device_id = None
            if vtherm_state.attributes:
                device_id = vtherm_state.attributes.get("device_id")
            
            # Search sensor entities for one with the attribute
            # Check if it's related to this device by device_id or entity_id pattern
            for entity_id, state in self._hass.states.async_all("sensor"):
                if not state.attributes:
                    continue
                    
                # Check if this sensor has the max_capacity_heat attribute
                if VTHERM_ATTR_MAX_CAPACITY_HEAT in state.attributes:
                    # Verify it belongs to the same device if device_id is available
                    if device_id and state.attributes.get("device_id") != device_id:
                        continue
                    
                    # Also check if entity_id contains the climate entity name
                    if climate_entity not in entity_id and climate_entity.replace("_", "") not in entity_id:
                        # Skip if it doesn't seem related to this climate entity
                        continue
                    
                    heat_rate_raw = state.attributes.get(VTHERM_ATTR_MAX_CAPACITY_HEAT)
                    if heat_rate_raw is not None:
                        try:
                            heat_rate = float(heat_rate_raw)
                            if heat_rate > 0:
                                _LOGGER.debug(
                                    "[%s] Found Heat Rate %.3f°C/h from sensor %s (discovered)",
                                    self._device_name,
                                    heat_rate,
                                    entity_id
                                )
                                return heat_rate
                        except (ValueError, TypeError):
                            pass
        
        # Fallback: try reading from climate entity (for backward compatibility)
        vtherm_state = self._hass.states.get(self._vtherm_entity_id)
        if vtherm_state:
            heat_rate_raw = get_vtherm_attribute(vtherm_state, VTHERM_ATTR_MAX_CAPACITY_HEAT)
            if heat_rate_raw is not None:
                try:
                    heat_rate = float(heat_rate_raw)
                    if heat_rate > 0:
                        _LOGGER.debug(
                            "[%s] Found Heat Rate %.3f°C/h from climate entity",
                            self._device_name,
                            heat_rate
                        )
                        return heat_rate
                except (ValueError, TypeError) as e:
                    _LOGGER.debug(
                        "[%s] Invalid Heat Rate value from climate entity: %s",
                        self._device_name,
                        heat_rate_raw,
                        exc_info=e
                    )
        
        # Log available sensor entities for debugging
        _LOGGER.debug(
            "[%s] max_capacity_heat attribute not found. Tried sensor entities: %s",
            self._device_name,
            ", ".join(possible_sensor_ids)
        )
        
        # Check if any sensor entities exist with auto_tpi in the name for debugging
        auto_tpi_sensors = [
            entity_id for entity_id, state in self._hass.states.async_all("sensor")
            if "auto_tpi" in entity_id.lower()
        ]
        if auto_tpi_sensors:
            _LOGGER.debug(
                "[%s] Found Auto TPI sensor entities: %s",
                self._device_name,
                ", ".join(auto_tpi_sensors)
            )
        
        return None
    
    def is_heating_active(self) -> bool:
        """Check if heating is currently active.
        
        According to requirements: heating is active when:
        1. hvac_mode == 'heat' (heating mode enabled)
        2. current_temperature < target_temperature (demand for heat)
        
        Returns:
            True if heating is ON, False otherwise
        """
        vtherm_state = self._hass.states.get(self._vtherm_entity_id)
        if not vtherm_state:
            return False
        
        # Check hvac_mode is 'heat'
        hvac_mode = vtherm_state.state
        if hvac_mode != "heat":
            return False
        
        # Check current temp is lower than target temp (v8.0.0+ compatible)
        current_temp = get_vtherm_attribute(vtherm_state, "current_temperature")
        target_temp = get_vtherm_attribute(vtherm_state, "temperature")
        
        if current_temp is None or target_temp is None:
            # If we can't determine temps, assume not heating
            return False
        
        try:
            return float(current_temp) < float(target_temp)
        except (ValueError, TypeError):
            return False
    
    def _get_float_state(self, entity_id: str | None) -> float | None:
        """Safely get float value from entity state.
        
        Args:
            entity_id: Entity ID to read
            
        Returns:
            Float value or None
        """
        if not entity_id:
            return None
        
        state = self._hass.states.get(entity_id)
        if not state:
            return None
        
        try:
            return float(state.state)
        except (ValueError, TypeError):
            return None

    # --- Accessors for application orchestration (historical data fetching) ---
    def get_hass(self):
        """Return the Home Assistant instance for adapters.
        
        Exposed for application layer orchestration that needs to construct
        historical data adapters. This keeps infrastructure concerns out of
        the domain while enabling coordinated use cases.
        """
        return self._hass

    def get_vtherm_entity_id(self) -> str:
        """Return the VTherm climate entity id."""
        return self._vtherm_entity_id

    def get_outdoor_temp_entity_id(self) -> str | None:
        """Return the outdoor temperature sensor entity id (optional)."""
        return self._outdoor_temp_entity_id

    def get_humidity_in_entity_id(self) -> str | None:
        """Return the indoor humidity sensor entity id (optional)."""
        return self._humidity_in_entity_id

    def get_humidity_out_entity_id(self) -> str | None:
        """Return the outdoor humidity sensor entity id (optional)."""
        return self._humidity_out_entity_id

    def get_cloud_cover_entity_id(self) -> str | None:
        """Return the cloud coverage sensor entity id (optional)."""
        return self._cloud_cover_entity_id
