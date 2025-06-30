from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User,
    JobSeekerProfile,
    JobSeekerService,
    CompanyProfile,
    IndividualClientProfile,
    SupporterProfile,
    WorkSpace,
    SupportTicket,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin"""

    list_display = [
        "username",
        "email",
        "role",
        "is_verified",
        "is_active",
        "date_joined",
    ]
    list_filter = ["role", "is_verified", "is_active", "date_joined"]
    search_fields = ["username", "email", "first_name", "last_name"]

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("role", "mobile_number", "is_verified")}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("role", "mobile_number", "email")}),
    )


class JobSeekerServiceInline(admin.TabularInline):
    model = JobSeekerService
    extra = 1


@admin.register(JobSeekerProfile)
class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "specialization",
        "field_of_work",
        "rating",
        "is_available",
        "is_employed",
    ]
    list_filter = [
        "specialization",
        "field_of_work",
        "experience_level",
        "is_available",
        "is_employed",
    ]
    search_fields = ["user__username", "user__email", "specialization", "field_of_work"]
    inlines = [JobSeekerServiceInline]

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "user",
                    "photo",
                    "specialization",
                    "field_of_work",
                    "date_of_birth",
                )
            },
        ),
        (
            "Professional Info",
            {"fields": ("experience_level", "bio", "rating", "expected_hourly_rate")},
        ),
        (
            "Status",
            {"fields": ("is_available", "is_employed", "weekly_applications_count")},
        ),
    )


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ["company_name", "user", "location", "company_type", "company_size"]
    list_filter = ["company_type", "company_size", "location"]
    search_fields = ["company_name", "user__username", "license_number"]

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "user",
                    "company_name",
                    "company_logo",
                    "location",
                    "company_type",
                )
            },
        ),
        (
            "Company Details",
            {
                "fields": (
                    "license_number",
                    "company_size",
                    "headquarters",
                    "company_bio",
                )
            },
        ),
        ("Online Presence", {"fields": ("website", "linkedin_url")}),
    )


@admin.register(IndividualClientProfile)
class IndividualClientProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "publisher_type", "business_name", "location"]
    list_filter = ["publisher_type", "location"]
    search_fields = ["user__username", "user__email", "business_name"]

    fieldsets = (
        ("Basic Info", {"fields": ("user", "publisher_type", "photo", "location")}),
        ("Business Info", {"fields": ("business_name", "business_description")}),
        ("Social Media", {"fields": ("linkedin_url", "twitter_url", "facebook_url")}),
    )


@admin.register(SupporterProfile)
class SupporterProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "country",
        "total_donations",
        "donation_count",
        "badge_level",
    ]
    list_filter = ["badge_level", "country"]
    search_fields = ["user__username", "user__email", "country"]
    readonly_fields = ["total_donations", "donation_count"]

    actions = ["update_badge_levels"]

    def update_badge_levels(self, request, queryset):
        for supporter in queryset:
            supporter.update_badge_level()
        self.message_user(
            request, f"Updated badge levels for {queryset.count()} supporters."
        )

    update_badge_levels.short_description = "Update badge levels"


@admin.register(WorkSpace)
class CoworkingSpaceAdmin(admin.ModelAdmin):
    list_display = ["name", "owner_name", "location", "has_power", "has_fast_internet"]
    list_filter = ["has_power", "has_fast_internet", "location"]
    search_fields = ["name", "owner_name", "location"]


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["user__username", "title", "description"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        ("Ticket Info", {"fields": ("user", "title", "status")}),
        ("Content", {"fields": ("description", "message")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
