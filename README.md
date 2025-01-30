# google-calendar modular service

This module implements the [rdk generic API](https://github.com/rdk/generic-api) in a [**coderscafe:calendar:google-calendar**](https://app.viam.com/module/coderscafe/google-calendar) model.
With this module, you can read and write events on your Google Calendar.

## Requirements

Ensure you have generated a service account file from the Google Cloud Console, if not follow the steps from [here](https://codelabs.viam.com/guide/pomodoro-bot/index.html?index=..%2F..index#3).

## Build and Run

To use this module, follow these instructions to [add a module from the Viam Registry](https://docs.viam.com/registry/configure/#add-a-modular-resource-from-the-viam-registry) and select the [`coderscafe:calendar:google-calendar` module](https://app.viam.com/module/coderscafe/google-calendar).

## Configure your generic

> [!NOTE]  
> Before configuring your generic, you must [create a machine](https://docs.viam.com/manage/fleet/machines/#add-a-new-machine).

* Navigate to the **Config** tab of your robot’s page in [the Viam app](https://app.viam.com/).
* Click on the **Services** subtab and search for `coderscafe:calendar:google-calendar`.
* Select the `coderscafe:calendar:google-calendar` model. 
* Enter a name for your generic service and click **Create**.
* Save and wait for the service to finish setup.

On the new service panel, copy and paste the following attribute template into your generic’s **Attributes** box:

```json
{
  "calendar_id": calendar-id,
  "service_account_file": path-of-service-account-json-file
}
```

> [!NOTE]  
> For more information, see [Configure a Robot](https://docs.viam.com/manage/configuration/).

### Attributes

The following attributes are available for `coderscafe:calendar:google-calendar` module:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `calendar_id` | string | **Required** |  ID of your Calendar |
| `service_account_file` | string | **Required** |  Path to your Service Account JSON file |

### Example Configuration

```json
{
  "calendar_id": calendar-id,
  "service_account_file": path-of-service-account-json-file
}
```
