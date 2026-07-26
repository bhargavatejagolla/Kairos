# Authorization Engine (RBAC)

KAIROS uses a robust, database-driven Role-Based Access Control (RBAC) engine that evaluates permissions decoupled from roles.

## Permission Structure
Permissions are fine-grained string keys defined in `app.core.permissions.Permission`, following the format `entity:action`. Examples include:
- `users:read`
- `users:create`
- `projects:update`
- `incidents:delete`

## Role Structure
Roles are collections of permissions stored in the database. Out-of-the-box, KAIROS provides standard roles:
- **Admin**: Has all permissions across the system.
- **Operator**: Read access to most entities, update access to incidents/projects, and alert acknowledgment.
- **Developer**: Read access to projects/incidents, update access to incidents.
- **Viewer**: Read-only access to basic entities.

## Authorization Flow
1. The user authenticates with a JWT.
2. `ActiveUserDep` loads the Current User.
3. Protected endpoints define dependencies like `Depends(require_permission("users:read"))`.
4. The `AuthorizationService` determines if the user has the required permission:
   - *(Future: Phase 7)* It looks up the user's `OrganizationMember` record for the active organization context.
   - It loads the Role assigned to that membership.
   - It checks if the requested permission exists within that Role's permission set.
5. If the permission exists, the endpoint executes. If not, a `PermissionDeniedError` (HTTP 403) is raised.

## API Reference
The RBAC API allows dynamic creation and modification of custom roles.

- `GET /api/v1/roles`: List all roles
- `POST /api/v1/roles`: Create a new custom role
- `GET /api/v1/roles/{id}`: View a role
- `PATCH /api/v1/roles/{id}`: Edit a role
- `DELETE /api/v1/roles/{id}`: Delete a role
- `POST /api/v1/roles/{id}/permissions`: Assign a permission to a role
- `DELETE /api/v1/roles/{id}/permissions/{perm_id}`: Remove a permission from a role

- `GET /api/v1/permissions`: List all available system permissions

## Adding a New Permission
Adding a new permission to the KAIROS system takes zero API code changes:
1. Define the permission string in `app/core/permissions.py`.
2. Map it to the default roles in `app/db/seeds/rbac.py` if needed.
3. Run the seed process using the seed runner.
4. Protect endpoints using `Depends(require_permission(Permission.NEW_PERMISSION.value))`.
